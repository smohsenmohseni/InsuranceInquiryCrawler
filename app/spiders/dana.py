# Standard imports
import json
from http.cookies import SimpleCookie

# Core imports.
from scrapy.http import FormRequest, JsonRequest, TextResponse

# Local imports.
from app.generics import GenericFormLoginSpider


class DanaInsuranceSpider(GenericFormLoginSpider):
    handle_httpstatus_list = [302]

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
        return json.loads(response.body)
