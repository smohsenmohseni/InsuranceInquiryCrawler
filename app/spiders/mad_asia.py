# Standard imports
import json
from typing import Any, Generator

# Core imports.
from scrapy.http import Request, FormRequest, TextResponse

# Local imports.
from app.generics import GenericSpider
from app.loaders.mad import MadInsuranceItemLoader


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
            meta={'handle_httpstatus_list': [500]},
            cookies=json.loads(response.body),
            callback=self.parse,
        )

    @staticmethod
    def parse(response: TextResponse, **kwargs: None) -> dict[str, str] | None:
        if response.status == 200:
            resp: dict[str, Any] = json.loads(response.body)
            data: dict[str, str | int] = resp['PreAuthEnabledPolicies'][0]
            loader = MadInsuranceItemLoader()
            loader.add_value('support', resp['IsUnderCov'])
            loader.add_value('end_date', data['CovEndDate'])
            loader.add_value('start_date', data['CovBeginDate'])
            loader.add_value('national_code', data['InsuredPersonNationalCode'])
            loader.add_value('customer_name', data['CustomerName'])
            loader.add_value('relationship', data['RelationTypeText'])
            return loader.load_item()
        return None
