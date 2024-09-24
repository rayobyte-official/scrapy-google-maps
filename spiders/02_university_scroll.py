from googlemaps.items import UniversityItemLoader
from parsel import Selector
from scrapy import Spider, Request
from scrapy_playwright.page import PageMethod


class UniversityScrollSpider(Spider):
    """This spider collects all universities in Nebraska, United States."""
    name = "university_scroll"

    def start_requests(self):
        yield Request(
            url="https://www.google.com/maps/search/university+in+nebraska,+United+States?hl=en-US",
            callback=self.parse_universities,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                # The next part is optional if there is no consent form to click through
                playwright_page_methods=[
                    PageMethod("wait_for_selector", selector="form"),
                    PageMethod("click", selector="button"),
                ],
            )
        )

    async def parse_universities(self, response):
        page = response.meta["playwright_page"]
        html = await page.content()
        while True:
            if "You've reached the end of the list." in html:
                break
            await page.get_by_role('feed').press("PageDown")
            await page.wait_for_timeout(500)
            html = await page.content()

        await page.close()

        sel = Selector(text=html)

        links = sel.css('div[role="feed"] > div > div > a')
        for link in links:
            yield response.follow(
                url=link,
                callback=self.parse_university,
                meta={
                    "playwright": True,
                }
            )

    async def parse_university(self, response):
        item = UniversityItemLoader(response=response)
        item.add_css('name', 'h1::text')
        item.add_xpath('rating', ".//*[contains(@aria-label,'stars')]/@aria-label")
        item.add_xpath('phone', '//button[contains(@aria-label, "Phone:")]/@aria-label')
        yield item.load_item()


