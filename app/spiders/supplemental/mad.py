# Standard imports
import json
from typing import Any, Generator

# Core imports.
from scrapy.http import Request, FormRequest, TextResponse

# Local imports.
from app.generics import GenericSpider
from app.loaders.mad import MadInsuranceItemLoader


class BaseMadSpider(GenericSpider):
    def info_name(self) -> str:
        return 'MAD_INSURANCE_INFO'

    def start_requests(self) -> Generator[FormRequest, None, None]:
        yield FormRequest(
            self.login_url,
            formdata=self.login_data,
            callback=self.inquiry_request,
        )

    def inquiry_request(self, response: TextResponse) -> Request:
        return Request(
            self.inquiry_url,
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


class MadAsiaInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=155, national_code=self.national_code)
        return super().inquiry_request(response)


class MadMaInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=150, national_code=self.national_code)
        return super().inquiry_request(response)


class MadRaziInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=151, national_code=self.national_code)
        return super().inquiry_request(response)


class MadAtiehInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=158, national_code=self.national_code)
        return super().inquiry_request(response)


class MadTaavonInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=159, national_code=self.national_code)
        return super().inquiry_request(response)


class MadNovinInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=178, national_code=self.national_code)
        return super().inquiry_request(response)


class MadMihanInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=155, national_code=self.national_code)
        return super().inquiry_request(response)


class MadArmanInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=273, national_code=self.national_code)
        return super().inquiry_request(response)


class MadParsianInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=543, national_code=self.national_code)
        return super().inquiry_request(response)


class MadAlborzInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=2063, national_code=self.national_code)
        return super().inquiry_request(response)


class MadSarmadInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=2498, national_code=self.national_code)
        return super().inquiry_request(response)


class MadSinaInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=3025, national_code=self.national_code)
        return super().inquiry_request(response)


class MadTejaratNoInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=3539, national_code=self.national_code)
        return super().inquiry_request(response)


class MadMoalemInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=5650, national_code=self.national_code)
        return super().inquiry_request(response)


class MadKosarInsuranceSpider(BaseMadSpider):
    def inquiry_request(self, response: TextResponse) -> Request:
        self.inquiry_url: str = self.inquiry_url.format(insurance_id=19023, national_code=self.national_code)
        return super().inquiry_request(response)
