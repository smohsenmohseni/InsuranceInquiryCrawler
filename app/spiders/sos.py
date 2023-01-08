# Standard imports
import json
from typing import Generator

# Core imports.
from scrapy.http import JsonRequest, TextResponse

# Local imports.
from app.generics import GenericSpider


class SosInsuranceSpider(GenericSpider):
    def start_requests(self) -> Generator[JsonRequest, None, None]:
        data_: dict[str, str] = {
            'serviceDate': '1401/10/16',
            'hospitalId': '153398',
            'nationalcode': self.national_code,
        }
        yield JsonRequest(self.inquiry_url, data=data_, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs: None) -> dict:
        response_model: list = json.loads(response.body.decode()).get('model')
        if response_model:
            return response_model[0]
        return {'status': 'not valid'}
