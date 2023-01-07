# Standard imports
import json
from typing import Generator

# Core imports.
from scrapy.http import Request, TextResponse

# Local imports.
from app.generics import GenericSpider


class TaminInsuranceSpider(GenericSpider):
    def start_requests(self) -> Generator[Request, None, None]:
        yield Request(self.inquiry_url.format(national_code=self.national_code), callback=self.parse)

    def parse(self, response: TextResponse, **kwargs: None) -> dict:
        return json.loads(response.body)
