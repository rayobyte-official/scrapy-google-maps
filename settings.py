BOT_NAME = "googlemaps"

SPIDER_MODULES = ["googlemaps.spiders"]
NEWSPIDER_MODULE = "googlemaps.spiders"

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 1

COOKIES_ENABLED = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": False,
}

PLAYWRIGHT_PROCESS_REQUEST_HEADERS = None

def should_abort_request(request):
    return (
            request.resource_type == "image"
            or any(
        x in request.url
        for x in [
            "gen_204",
            "/maps/vt",
        ]
    )
            or any(ext in request.url for ext in [".jpg", ".png", ".jpeg", ".gif", ".svg", ".webp", ".ico"])
    )

PLAYWRIGHT_ABORT_REQUEST = should_abort_request
