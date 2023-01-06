# Core imports.
from scrapy import Spider

# Local imports.
from core.helpers import to_snake_case


class BaseSpiderGeneric(Spider):
    @classmethod
    def name(cls):
        return to_snake_case(cls.__name__.replace('Spider', ''))

    def parse(self, response, **kwargs):
        ...
