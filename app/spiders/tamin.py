# Standard imports
import json

# Local imports.
from app.generics.base import BaseSpiderGeneric


class TaminInsuranceSpider(BaseSpiderGeneric):
    start_urls = ['https://medical.tamin.ir/api/medical-support/v2.0/2051057540']

    def parse(self, response, **kwargs):
        return json.loads(response.body)
