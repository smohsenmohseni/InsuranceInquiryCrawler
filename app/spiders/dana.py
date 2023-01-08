# Standard imports
import json
from typing import Generator
from http.cookies import SimpleCookie

# Core imports.
from scrapy.http import Request, FormRequest, JsonRequest, TextResponse

# Local imports.
from app.generics import GenericSpider


class DanaInsuranceSpider(GenericSpider):
    handle_httpstatus_list = [302]

    def start_requests(self) -> Generator[Request, None, None]:
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

    def parse(self, response: TextResponse, **kwargs: None) -> dict:
        """
        :success: return dict with status success
        :fail: return dict with status fail
        """
        # TODO: use item and item loader to check insurance
        return json.loads(response.body)
