# Standard imports
import json

# Core imports.
from scrapy.http import Request

# Local imports.
from app.generics import GenericSpider


class TaminInsuranceSpider(GenericSpider):
    def start_requests(self):
        yield Request(self.inquiry_url.format(national_code=self.national_code), callback=self.parse)

    def parse(self, response, **kwargs):
        return json.loads(response.body)
