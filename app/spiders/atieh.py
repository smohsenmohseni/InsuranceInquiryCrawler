# Standard imports
import re

# Core imports.
from scrapy.http import FormRequest

# Local imports.
from app.generics import GenericFormLoginSpider


class AtiehInsuranceSpider(GenericFormLoginSpider):
    custom_settings = {'REDIRECT_ENABLED': True}

    def login_request(self, response):
        return FormRequest.from_response(
            response,
            formdata=self.login_data,
            meta={'handle_httpstatus_list': [302]},
            callback=self.inquiry_request,
        )

    def inquiry_request(self, response):
        token = re.findall('TGC=[A-Za-z0-9._]*', response.headers.to_string().decode())[0].replace('TGC=', '')
        return FormRequest(
            self.inquiry_url,
            method='POST',
            cookies={'TGC': token},
            formdata={
                'nationalCode': self.national_code,
                'requestType': 'outpatient',
                '_eventId': '',
            },
            dont_filter=True,
            meta={
                'dont_redirect': False,
            },
            callback=self.parse,
        )

    def parse(self, response, **kwargs):
        rows = response.css(
            '#policyInfoPanelBox-collapse div.col-lg-4.col-md-4.col-sm-6.col-xs-12 '
            'p.text-secondary.pd-top-label-body.iransans'
        )
        values = rows.css('*::text').getall()
        yield {
            'name': values[0],
            'national_code': values[1],
            'father_name': values[2],
            'birthdate': values[4],
            'insurance_name': values[6],
            'basic_insurance_name': values[12],
        }
