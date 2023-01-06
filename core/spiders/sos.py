# Standard imports
import json

# Core imports.
from scrapy import Spider
from scrapy.http import Request, JsonRequest


class SOSInsuranceSpider(Spider):
    name = 'sos_insurance'
    login_url = 'https://carewrapper.iranassistance.com/Auth/Authentication/LoginUser'
    inquiry_url = 'https://carewrapper.iranassistance.com/api/CareCenter/GetContractList'

    # def start_requests(self):
    #     data_ = {
    #         'recaptchaResponse': 'NotResolved',
    #         'username': '153398',
    #         'password': '751932',
    #         'sosCaptchaResponse': '3',
    #     }
    #     yield JsonRequest(self.login_url, data=data_, callback=self.inquiry_request)
    #
    # def inquiry_request(self, response):
    #     token = json.loads(response.body.decode()).get('token')
    #     data_ = {
    #         'serviceDate': '1401/10/16', 'hospitalId': '153398', 'nationalcode': '2593158999'
    #     }
    #     headers_ = {
    #         'Authorization': f'Bearer {token}'
    #     }
    #     yield JsonRequest(self.inquiry_url, data=data_, callback=self.parse)

    def start_requests(self):
        data_ = {
            'serviceDate': '1401/10/16',
            'hospitalId': '153398',
            'nationalcode': '2593158999',
        }
        yield JsonRequest(self.inquiry_url, data=data_, callback=self.parse)

    def parse(self, response, **kwargs):
        yield json.loads(response.body.decode()).get('model')[0]
