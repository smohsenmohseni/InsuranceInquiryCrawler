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
        )

    def inquiry_request(self, response, **kwargs):
        yield Request(
            self.inquiry_url.format(national_code=self.national_code),
            callback=self.parse,
            cookies=json.loads(response.body),
        )

    @staticmethod
    def parse(response, **kwargs):
        return json.loads(response.body)
