# Standard imports
import json

# Core imports.
from scrapy.http import JsonRequest

# Local imports.
from app.generics import BaseSpiderGeneric


class SOSInsuranceSpider(BaseSpiderGeneric):
    login_url = 'https://carewrapper.iranassistance.com/Auth/Authentication/LoginUser'
    inquiry_url = 'https://carewrapper.iranassistance.com/api/CareCenter/GetContractList'

    def start_requests(self):
        data_ = {
            'serviceDate': '1401/10/16',
            'hospitalId': '153398',
            'nationalcode': '2593158999',
        }
        yield JsonRequest(self.inquiry_url, data=data_, callback=self.parse)

    def parse(self, response, **kwargs):
        yield json.loads(response.body.decode()).get('model')[0]
