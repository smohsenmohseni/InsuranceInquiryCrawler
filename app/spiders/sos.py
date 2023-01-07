# Standard imports
import json

# Core imports.
from scrapy.http import JsonRequest

# Local imports.
from app.generics import GenericSpider


class SosInsuranceSpider(GenericSpider):
    def start_requests(self):
        data_ = {
            'serviceDate': '1401/10/16',
            'hospitalId': '153398',
            'nationalcode': self.national_code,
        }
        yield JsonRequest(self.inquiry_url, data=data_, callback=self.parse)

    def parse(self, response, **kwargs):
        yield json.loads(response.body.decode()).get('model')[0]
