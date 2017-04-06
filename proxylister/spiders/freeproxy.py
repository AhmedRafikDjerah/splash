import scrapy
from scrapy_splash import SplashRequest

class FreeProxyLister(scrapy.Spider):
    name = 'proxylist'

    def start_requests(self):
        yield SplashRequest(url='http://freeproxylists.net/fr/', callback=self.parse, endpoint='render.html')

    def parse(self, response):
        for data in response.css("tbody tr"):
            yield {
                'ip': data.css("td:nth-child(1) a::text").extract_first()
            }

        next_page = response.css(".page a:last-child::attr(href)").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield SplashRequest(url=next_page, callback=self.parse, endpoint='render.html')
