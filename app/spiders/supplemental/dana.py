# Standard imports
import json
import time
from typing import Any, Optional
from http.cookies import SimpleCookie

# Core imports.
from scrapy.http import Request, FormRequest, JsonRequest, TextResponse

# Third-party imports.
from jdatetime import datetime

# Local imports.
from core.typing import StrIntUnion, GeneratorWithoutSendReturn
from app.generics import GenericSpider
from app.loaders.dana import DanaInsuranceItemLoader


class DanaInsuranceSpider(GenericSpider):
    handle_httpstatus_list = [302]
    remaining_ceiling_url: str
    franchise_url: str
    login_cookie: dict

    def start_requests(self) -> GeneratorWithoutSendReturn[Request]:
        yield Request(self.login_url, callback=self.login_request)

    def login_request(self, response: TextResponse) -> FormRequest:
        return FormRequest.from_response(
            response,
            formdata=self.login_data,
            callback=self.set_cookie,
        )

    def set_cookie(self, response: TextResponse) -> Request | FormRequest:
        c: SimpleCookie = SimpleCookie()
        c.load(response.headers.get('set-cookie').decode())
        self.login_cookie = {'.ASPXAUTH': c['.ASPXAUTH'].value}
        return self.inquiry_request(response)

    def inquiry_request(self, response: TextResponse) -> JsonRequest:
        c: SimpleCookie = SimpleCookie()
        c.load(response.headers.get('set-cookie').decode())
        return JsonRequest(
            self.inquiry_url.format(national_code=self.national_code),
            callback=self.franchise_request,
            cookies=self.login_cookie,
        )

    def franchise_request(self, response: TextResponse) -> Optional[JsonRequest]:
        response_data: dict[str, Any] = json.loads(response.body)
        if response_data['Success']:
            loader = DanaInsuranceItemLoader()
            data: dict[str, StrIntUnion] = response_data['Data']
            self.extract_data(data, loader)
            return JsonRequest(
                self.franchise_url.format(national_code=self.national_code),
                method='GET',
                data={
                    "CodeRayaneBimename": loader.get_output_value('policy_id'),
                    "CodeRayaneBimeShodeCmn": loader.get_output_value('id'),
                    "TarikhBastari": datetime.now().strftime('%Y/%m/%d'),
                    "tarhId": loader.get_output_value('insured_plan'),
                    "tarikhShoroeBimename": "1401%2F07%2F01",
                    "CodeRayaneGorupBimariBimeGar": 4531,
                    "CodeRayaneMarkazDarmaniVar": 425,
                    "_": int(time.time()),
                    "NoeMoareinameID": 4,
                },
                callback=self.remaining_ceiling_request,
                cb_kwargs={'loader': loader},
                cookies=self.login_cookie,
            )
        return None

    def remaining_ceiling_request(
        self, response: TextResponse, loader: DanaInsuranceItemLoader
    ) -> Optional[JsonRequest]:
        response_data: dict[str, Any] = json.loads(response.body)
        if response_data['Success']:
            data: dict[str, StrIntUnion] = response_data['Data']
            self.extract_data(data, loader)
            return JsonRequest(
                self.remaining_ceiling_url,
                method='GET',
                data={
                    "NoeBimenameId": loader.get_output_value('policy_type_id'),
                    "CodeRayaneBimename": loader.get_output_value('policy_id'),
                    "CodeRayaneBimeShode": loader.get_output_value('insured'),
                    "CodeRayaneBimeShodeCmn": loader.get_output_value('id'),
                    "TarikhBastari": datetime.now().strftime('%Y/%m/%d'),
                    "CodeRayaneGorupBimariBimeGar": 4531,
                    "_": int(time.time()),
                },
                cb_kwargs={'loader': loader},
                cookies=self.login_cookie,
                callback=self.parse,
            )
        return None

    def parse(self, response: TextResponse, **kwargs: DanaInsuranceItemLoader) -> Optional[dict]:
        response_data: dict[str, Any] = json.loads(response.body)
        if response_data['Success']:
            loader = kwargs['loader']
            self.extract_data(response_data, loader)
            return loader.load_item()
        return None

    @staticmethod
    def extract_data(data: dict, loader: DanaInsuranceItemLoader) -> None:
        loader.add_value('id', data.get('Id'))
        loader.add_value('insured', data.get('BSId'))
        loader.add_value('policy_id', data.get('BnID'))
        loader.add_value('gender', data.get('jensText'))
        loader.add_value('first_name', data.get('Name'))
        loader.add_value('end_date', data.get('EndDate'))
        loader.add_value('last_name', data.get('Family'))
        loader.add_value('franchise', data.get('Franshiz'))
        loader.add_value('begin_date', data.get('BeginDate'))
        loader.add_value('birth_year', data.get('BirthYear'))
        loader.add_value('fullname', data.get('BsDisplyName'))
        loader.add_value('remaining_ceiling', data.get('Data'))
        loader.add_value('father_name', data.get('FatherName'))
        loader.add_value('relationship', data.get('NesbatText'))
        loader.add_value('national_code', data.get('CodeMelli'))
        loader.add_value('policy_type_id', data.get('NoeBimenameId'))
        loader.add_value('insured_plan', data.get('TarhBimeshodeId'))
