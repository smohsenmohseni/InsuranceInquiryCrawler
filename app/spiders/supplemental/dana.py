# Standard imports
import json
from typing import Any, Optional
from http.cookies import SimpleCookie

# Core imports.
from scrapy.http import Request, FormRequest, JsonRequest, TextResponse

# Local imports.
from core.typing import StrIntUnion, GeneratorWithoutSendReturn
from app.generics import GenericSpider
from app.loaders.dana import DanaInsuranceItemLoader


class DanaInsuranceSpider(GenericSpider):
    handle_httpstatus_list = [302]
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
            cookies=self.login_cookie,
            callback=self.parse,
        )

    def franchise_request(self, response: TextResponse) -> JsonRequest:
        return JsonRequest(
            self.franchise_url.format(national_code=self.national_code),
            cookies=self.login_cookie,
            callback=self.parse,
        )

    def parse(self, response: TextResponse, **kwargs: None) -> Optional[dict]:
        response_data: dict[str, Any] = json.loads(response.body)
        if response_data['Success']:
            loader = DanaInsuranceItemLoader()
            data: dict[str, StrIntUnion] = response_data['Data']
            self.extract_data(data, loader)
            return loader.load_item()
        return None

    @staticmethod
    def extract_data(data: dict, loader: DanaInsuranceItemLoader) -> None:
        loader.add_value('gender', data['jensText'])
        loader.add_value('first_name', data['Name'])
        loader.add_value('end_date', data['EndDate'])
        loader.add_value('last_name', data['Family'])
        loader.add_value('begin_date', data['BeginDate'])
        loader.add_value('birth_year', data['BirthYear'])
        loader.add_value('fullname', data['BsDisplyName'])
        loader.add_value('father_name', data['FatherName'])
        loader.add_value('relationship', data['NesbatText'])
        loader.add_value('national_code', data['CodeMelli'])
