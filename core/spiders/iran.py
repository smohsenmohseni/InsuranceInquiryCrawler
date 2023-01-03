import re

from scrapy import Spider
from scrapy.http import FormRequest, Request


class IranInsuranceSpider(Spider):
    name = 'iran_insurance'
    login_url = 'https://darman.iraninsurance.ir/dms-cas/login'
    inquiry_url = (
        'https://totalapp2.dana-insurance.ir/Sepad1/Fanavaran/'
        'GetDataBimenameBimeShodeFanByCodeMeliTarikh?tarikhHazine=1401/10/13&CodeMelli=0015376461'
    )

    def start_requests(self):
        yield Request(self.login_url, dont_filter=True, callback=self.login_request)

    def login_request(self, response):
        return FormRequest.from_response(
            response,
            formdata={'username': '444431488', 'password': 'moein999'},
            callback=self.inquiry_request,
        )

    @staticmethod
    def inquiry_request(response):
        split_cookie = re.split('; |,', response.headers.to_unicode_dict()['set-cookie'])
        print(split_cookie)

    def parse(self, response, **kwargs): ...
