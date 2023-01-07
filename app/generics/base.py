# Core imports.
from scrapy import Spider
from scrapy.http import Request

# Local imports.
from app.constants import info
from app.helpers.transformers import to_snake_case


class GenericSpider(Spider):
    login_url: str
    inquiry_url: str
    login_data: dict
    custom_settings: dict

    def __init__(self, *args, **kwargs):
        self.__dict__.update(getattr(info, f'{self.name()}_info'.upper(), {}))
        super().__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        ...

    @classmethod
    def name(cls):
        return to_snake_case(cls.__name__.replace('Spider', ''))


class GenericFormLoginSpider(GenericSpider):
    def start_requests(self):
        yield Request(self.login_url, dont_filter=True, callback=self.login_request)

    def login_request(self, response):
        ...
