# Standard imports
import json
from typing import Generator

# Core imports.
from scrapy.http import Request, FormRequest, TextResponse

# Local imports.
from app.generics import GenericSpider


class MadAsiaInsuranceSpider(GenericSpider):
    def start_requests(self) -> Generator[FormRequest, None, None]:
        yield FormRequest(
            self.login_url,
            formdata=self.login_data,
            callback=self.inquiry_request,
        )

    def inquiry_request(self, response: TextResponse) -> Request:
        return Request(
            self.inquiry_url.format(national_code=self.national_code),
            callback=self.parse,
            cookies=json.loads(response.body),
        )

    @staticmethod
    def parse(response: TextResponse, **kwargs: None) -> dict:
        return json.loads(response.body)
