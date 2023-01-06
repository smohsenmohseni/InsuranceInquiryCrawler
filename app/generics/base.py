# Core imports.
from scrapy import Spider
from scrapy.http import Request

# Local imports.
from core.helpers import to_snake_case


class BaseSpiderGeneric(Spider):
    login_url: str
    inquiry_url: str
    custom_settings: dict

    @classmethod
    def name(cls):
        return to_snake_case(cls.__name__.replace('Spider', ''))

    def parse(self, response, **kwargs):
        ...


class FormLoginSpider(BaseSpiderGeneric):
    def start_requests(self):
        yield Request(self.login_url, dont_filter=True, callback=self.login_request)

    def login_request(self, response):
        ...
