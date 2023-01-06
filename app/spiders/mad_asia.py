# Standard imports
import json

# Core imports.
from scrapy.http import Request, FormRequest

# Local imports.
from app.generics import BaseSpiderGeneric


class MadAsiaInsuranceSpider(BaseSpiderGeneric):
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
        yield FormRequest(self.login_url, formdata=_data, callback=self.inquiry_request, dont_filter=True)

    def inquiry_request(self, response, **kwargs):
        yield Request(self.inquiry_url, callback=self.parse, cookies=json.loads(response.body), dont_filter=True)

    @staticmethod
    def parse(response, **kwargs):
        return json.loads(response.body)
