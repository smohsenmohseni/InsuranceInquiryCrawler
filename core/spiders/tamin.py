# Standard imports
import json

# Core imports.
from scrapy import Spider
from scrapy.http import Request


class TaminInsuranceSpider(Spider):
    name = 'tamin_insurance'
    start_urls = ['https://medical.tamin.ir/api/medical-support/v2.0/2051057540']

    def parse(self, response, **kwargs):
        return json.loads(response.body)
