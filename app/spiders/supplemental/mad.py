# Standard imports
import json
from typing import Any, Generator

# Core imports.
from scrapy.http import Request, FormRequest, TextResponse

# Local imports.
from app.generics import GenericSpider
from app.loaders.mad import MadInsuranceItemLoader


class BaseMadSpider(GenericSpider):
    insurance_id: int

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
            self.inquiry_url.format(insurance_id=self.insurance_id, national_code=self.national_code),
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
    insurance_id = 155


class MadMaInsuranceSpider(BaseMadSpider):
    insurance_id = 150


class MadRaziInsuranceSpider(BaseMadSpider):
    insurance_id = 151


class MadAtiehInsuranceSpider(BaseMadSpider):
    insurance_id = 158


class MadTaavonInsuranceSpider(BaseMadSpider):
    insurance_id = 159


class MadNovinInsuranceSpider(BaseMadSpider):
    insurance_id = 178


class MadMihanInsuranceSpider(BaseMadSpider):
    insurance_id = 155


class MadArmanInsuranceSpider(BaseMadSpider):
    insurance_id = 273


class MadParsianInsuranceSpider(BaseMadSpider):
    insurance_id = 543


class MadAlborzInsuranceSpider(BaseMadSpider):
    insurance_id = 2063


class MadSarmadInsuranceSpider(BaseMadSpider):
    insurance_id = 2498


class MadSinaInsuranceSpider(BaseMadSpider):
    insurance_id = 3025


class MadTejaratNoInsuranceSpider(BaseMadSpider):
    insurance_id = 3539


class MadMoalemInsuranceSpider(BaseMadSpider):
    insurance_id = 5650


class MadKosarInsuranceSpider(BaseMadSpider):
    insurance_id = 19023
