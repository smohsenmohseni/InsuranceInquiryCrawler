# Standard imports
import json

# Core imports.
from scrapy.http import FormRequest, JsonRequest

# Local imports.
from app.generics import GenericFormLoginSpider


class DanaInsuranceSpider(GenericFormLoginSpider):
    handle_httpstatus_list = [302]

    def login_request(self, response):
        yield FormRequest.from_response(
            response,
            formdata=self.login_data,
            callback=self.inquiry_request,
        )

    def inquiry_request(self, response, **kwargs):
        unicode_dict = response.headers.to_unicode_dict()
        access_cookie = unicode_dict['set-cookie'].split(';', 1)[0].split('=')
        access_cookie = {access_cookie[0]: access_cookie[1]}
        yield JsonRequest(self.inquiry_url, cookies=access_cookie, callback=self.parse)

    def parse(self, response, **kwargs):
        return json.loads(response.body)
