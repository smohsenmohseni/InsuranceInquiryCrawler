# Standard imports
import json

# Core imports.
from scrapy.http import Request, FormRequest, JsonRequest

# Local imports.
from app.generics.base import BaseSpiderGeneric


class DanaInsuranceSpider(BaseSpiderGeneric):
    handle_httpstatus_list = [302]
    login_url = 'https://totalapp2.dana-insurance.ir/Sepad1/Security'
    inquiry_url = (
        'https://totalapp2.dana-insurance.ir/Sepad1/Fanavaran/'
        'GetDataBimenameBimeShodeFanByCodeMeliTarikh?tarikhHazine=1401/10/13&CodeMelli=0015376461'
    )

    def start_requests(self):
        yield Request(self.login_url, dont_filter=True, callback=self.login_request)

    def login_request(self, response):
        yield FormRequest.from_response(
            response,
            formdata={'NameKarbari': 'mp1201451', 'RamzeObor': 'moein999'},
            callback=self.inquiry_request,
        )

    def inquiry_request(self, response, **kwargs):
        unicode_dict = response.headers.to_unicode_dict()
        access_cookie = unicode_dict['set-cookie'].split(';', 1)[0].split('=')
        access_cookie = {access_cookie[0]: access_cookie[1]}
        yield JsonRequest(self.inquiry_url, cookies=access_cookie, callback=self.parse)

    def parse(self, response, **kwargs):
        return json.loads(response.body)
