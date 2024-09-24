from googlemaps.items import UniversityItemLoader
from parsel import Selector
from scrapy import Spider, Request
from scrapy_playwright.page import PageMethod
from urllib.parse import quote_plus


class UniversityAllSpider(Spider):
    """This spider collects all universities in the United States."""
    name = "university_all"

    def start_requests(self):
        yield Request(
            url="https://www.google.com/maps?hl=en-US",
            callback=self.parse_consent,
            meta=dict(
                playwright=True,
                # The next part is optional if there is no consent form to click through
                playwright_page_methods=[
                    PageMethod("wait_for_selector", selector="form"),
                    PageMethod("click", selector="button"),
                ],
            )
        )

    def parse_consent(self, response):
        us_states = [
            "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
            "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
            "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
            "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
            "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
            "New Hampshire", "New Jersey", "New Mexico", "New York",
            "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
            "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
            "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
            "West Virginia", "Wisconsin", "Wyoming"
        ]

        for state in us_states:
            yield Request(
                url=f"https://www.google.com/maps/search/university+in+{quote_plus(state)},+United+States?hl=en-US",
                callback=self.parse_universities,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
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

    def parse_university(self, response):
        item = UniversityItemLoader(response=response)
        item.add_css('name', 'h1::text')
        item.add_xpath('rating', ".//*[contains(@aria-label,'stars')]/@aria-label")
        item.add_xpath('phone', '//button[contains(@aria-label, "Phone:")]/@aria-label')
        yield item.load_item()
