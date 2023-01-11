# Standard imports
import json
from typing import Generator

# Core imports.
from scrapy.http import Request, TextResponse

# Local imports.
from app.generics import GenericSpider
from app.loaders.tamin import TaminInsuranceItemLoader


class TaminInsuranceSpider(GenericSpider):
    def start_requests(self) -> Generator[Request, None, None]:
        yield Request(self.inquiry_url.format(national_code=self.national_code), callback=self.parse)

    def parse(self, response: TextResponse, **kwargs: None) -> dict[str, bool] | None:
        result: dict = json.loads(response.body)['data']['result']
        if result:
            loader = TaminInsuranceItemLoader()
            loader.add_value('result', result)
            return loader.load_item()
        return None
