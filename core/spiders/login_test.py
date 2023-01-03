# Standard imports
import json

# Core imports.
import scrapy
from scrapy.http import Request, FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login_to'
    login_url = 'https://mccp.iraneit.com/core/connect/token'
    inquiry_url = (
        "https://mccp.iraneit.com/odata/MCClaimProc/preAuthEnabledPolicy/"
        "getInsuredPersonPolicyInfo(corpId=155,nationalCodeOrId='2051057540',type='nationalcode')?$top=1"
    )

    def start_requests(self):
        _data = {
            'scope': 'openid profile user_info',
            'grant_type': 'password',
            'username': 'l.tehran11001',
            'password': 'abc123',
            'client_id': 'MCClaimProc-ResOwner',
            'client_secret': 'secret',
        }
        yield FormRequest(self.login_url, formdata=_data, callback=self.parse)

    def parse(self, response, **kwargs):
        yield Request(self.inquiry_url, callback=self.parse2, cookies=json.loads(response.body))

    @staticmethod
    def parse2(response, **kwargs):
        return json.loads(response.body)
