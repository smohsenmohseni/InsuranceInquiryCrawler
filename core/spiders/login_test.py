# Standard imports
import json

# Core imports.
import scrapy
from scrapy.http import Request, FormRequest, JsonRequest


class LoginSpider(scrapy.Spider):
    name = 'login_to'
    start_urls = ['https://mccp.iraneit.com/core/connect/token']
    headers_ = {
        'user-agent': (
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        ),
        'origin': 'https://mccp.iraneit.com',
        'referer': 'https://mccp.iraneit.com/',
    }
    meta_ = {'dont_redirect': True, 'handle_httpstatus_list': [302, 401]}

    def start_requests(self):
        _data = {
            'scope': 'openid profile user_info',
            'grant_type': 'password',
            'username': 'l.tehran11001',
            'password': 'abc123',
            'client_id': 'MCClaimProc-ResOwner',
            'client_secret': 'secret',
        }
        req = FormRequest(
            self.start_urls[0], formdata=_data, headers=self.headers_, callback=self.parse, meta=self.meta_
        )
        yield req

    def parse(self, response, **kwargs):
        _url = (
            "https://mccp.iraneit.com/odata/MCClaimProc/preAuthEnabledPolicy/getInsuredPersonPolicyInfo"
            "(corpId=155,nationalCodeOrId='2051057540',type='nationalcode')?$top=1"
        )
        headers_with_cookie = dict()
        headers_with_cookie.update(self.headers_)
        headers_with_cookie.update(json.loads(response.body))
        headers_with_cookie.update(
            {
                'MCCP_ARR': '753befbf0e269336bbc36a7115522b190547b2e11c6a3b0aa89bad9cbdad411d',
                'accept': 'application/json;q = 0.9, */*;q=0.1',
            }
        )
        req = JsonRequest(_url, headers=headers_with_cookie, callback=self.parse2, meta=self.meta_)
        yield req

    def parse2(self, response, **kwargs):
        print(response.status)
        print(response.request.headers)
