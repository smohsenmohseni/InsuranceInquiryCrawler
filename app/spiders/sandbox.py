# Local imports.
from app.generics.base import BaseSpiderGeneric


class SandBoxSpider(BaseSpiderGeneric):
    start_urls = ['https://www.google.com/']

    def parse(self, response, **kwargs):
        pass
