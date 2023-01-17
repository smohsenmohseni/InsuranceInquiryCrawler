# Standard imports
import json
from typing import Any, Optional
from http.cookies import SimpleCookie

# Core imports.
from scrapy.http import Request, FormRequest, JsonRequest, TextResponse

# Local imports.
from core.typing import GeneratorWithoutSendReturn
from app.generics import GenericSpider
from app.loaders.dana import DanaInsuranceItemLoader


class DanaInsuranceSpider(GenericSpider):
    handle_httpstatus_list = [302]

    def start_requests(self) -> GeneratorWithoutSendReturn[Request]:
        yield Request(self.login_url, callback=self.login_request)

    def login_request(self, response: TextResponse) -> FormRequest:
        return FormRequest.from_response(
            response,
            formdata=self.login_data,
            callback=self.inquiry_request,
        )

    def inquiry_request(self, response: TextResponse) -> JsonRequest:
        c: SimpleCookie = SimpleCookie()
        c.load(response.headers.get('set-cookie').decode())
        return JsonRequest(
            self.inquiry_url.format(national_code=self.national_code),
            cookies={'.ASPXAUTH': c['.ASPXAUTH'].value},
            callback=self.parse,
        )

    def parse(self, response: TextResponse, **kwargs: None) -> Optional[dict]:
        response_data: dict[str, Any] = json.loads(response.body)
        if response_data['Success']:
            loader = DanaInsuranceItemLoader()
            total_data: dict[str, str | int] = response_data['Data']
            loader.add_value('gender', total_data['jensText'])
            loader.add_value('fullname', total_data['BsDisplyName'])
            loader.add_value('end_date', total_data['EndDate'])
            loader.add_value('last_name', total_data['Family'])
            loader.add_value('begin_date', total_data['BeginDate'])
            loader.add_value('first_name', total_data['Name'])
            loader.add_value('birth_year', total_data['BirthYear'])
            loader.add_value('father_name', total_data['FatherName'])
            loader.add_value('relationship', total_data['NesbatText'])
            loader.add_value('national_code', total_data['CodeMelli'])
            return loader.load_item()
        return None
