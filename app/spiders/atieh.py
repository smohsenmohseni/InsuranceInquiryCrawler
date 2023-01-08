# Standard imports
from typing import Generator
from http.cookies import SimpleCookie

# Core imports.
from scrapy.http import Request, FormRequest, TextResponse

# Local imports.
from app.generics import GenericSpider


class AtiehInsuranceSpider(GenericSpider):
    custom_settings = {'REDIRECT_ENABLED': True}

    def start_requests(self) -> Generator[Request, None, None]:
        yield Request(self.login_url, callback=self.login_request)

    def login_request(self, response: TextResponse) -> FormRequest:
        return FormRequest.from_response(
            response,
            formdata=self.login_data,
            callback=self.inquiry_request,
        )

    def inquiry_request(self, response: TextResponse) -> FormRequest:
        c: SimpleCookie = SimpleCookie()
        c.load(response.request.headers.get('Cookie').decode())
        return FormRequest(
            self.inquiry_url,
            method='POST',
            cookies={'JSESSIONID': c['JSESSIONID'].value},
            formdata={
                'nationalCode': self.national_code,
                'requestType': 'outpatient',
                '_nonav': '',
            },
            callback=self.parse,
        )

    def parse(self, response: TextResponse, **kwargs: None) -> dict:
        rows = response.css(
            '#policyInfoPanelBox-collapse div.col-lg-4.col-md-4.col-sm-6.col-xs-12 '
            'p.text-secondary.pd-top-label-body.iransans'
        )
        values: list[str] = rows.css('*::text').getall()
        return {
            'name': values[0],
            'national_code': values[1],
            'father_name': values[2],
            'birthdate': values[4],
            'insurance_name': values[6],
            'basic_insurance_name': values[12],
        }
