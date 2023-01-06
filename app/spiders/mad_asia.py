# Standard imports
import json

# Core imports.
from scrapy.http import Request, FormRequest

# Local imports.
from app.generics import GenericSpider


class MadAsiaInsuranceSpider(GenericSpider):
    def start_requests(self):
        yield FormRequest(
            self.login_url,
            formdata=self.login_data,
            callback=self.inquiry_request,
            dont_filter=True,
        )

    def inquiry_request(self, response, **kwargs):
        yield Request(
            self.inquiry_url,
            callback=self.parse,
            cookies=json.loads(response.body),
            dont_filter=True,
        )

    @staticmethod
    def parse(response, **kwargs):
        return json.loads(response.body)
