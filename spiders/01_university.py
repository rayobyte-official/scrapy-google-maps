from googlemaps.items import UniversityItemLoader
from scrapy import Spider, Request
from scrapy_playwright.page import PageMethod


class UniversityOnePageSpider(Spider):
    """This spider collects only the first result page of universities in Nebraska, United States."""
    name = "university_one_page"

    def start_requests(self):
        yield Request(
            url="https://www.google.com/maps/search/university+in+nebraska,+United+States?hl=en-US",
            callback=self.parse_universities,
            meta=dict(
                playwright=True,
                # The next part is optional if there is no consent form to click through
                playwright_page_methods=[
                    PageMethod("wait_for_selector", selector="form"),
                    PageMethod("click", selector="button"),
                ],
            )
        )

    def parse_universities(self, response):
        links = response.css('div[role="feed"] > div > div > a')
        for link in links:
            yield response.follow(
                url=link,
                callback=self.parse_university,
                meta={
                    "playwright": True,
                }
            )

    def parse_university(self, response):
        item = UniversityItemLoader(response=response)
        item.add_css('name', 'h1::text')
        item.add_xpath('rating', ".//*[contains(@aria-label,'stars')]/@aria-label")
        item.add_xpath('phone', '//button[contains(@aria-label, "Phone:")]/@aria-label')
        yield item.load_item()

