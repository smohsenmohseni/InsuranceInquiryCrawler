# Standard imports
import json
from typing import Generator
from http.cookies import SimpleCookie

# Core imports.
from scrapy.http import Request, FormRequest, TextResponse

# Local imports.
from app.generics import GenericSpider
from app.loaders.atieh import AtiehInsuranceItemLoader
from app.helpers.decorator import disable_cache


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

    @disable_cache
    def inquiry_request(self, response: TextResponse) -> FormRequest:
        c: SimpleCookie = SimpleCookie()
        c.load(response.request.headers.get('Cookie').decode())
        yield FormRequest(
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

    def parse(self, response: TextResponse, **kwargs: None) -> Generator[dict, None, None] | None:
        if response.url.endswith('outpatient'):
            loader = AtiehInsuranceItemLoader(selector=response.selector)
            loader.add_css('insurer', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(8) p *::text')
            loader.add_css('fullname', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(1) p *::text')
            loader.add_css('birthdate', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(5) p *::text')
            loader.add_css('father_name', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(3) p *::text')
            loader.add_css('relationship', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(4) p *::text')
            loader.add_css('national_code', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(2) p *::text')
            loader.add_css('customer_group', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(11) p *::text')
            loader.add_css('insurance_name', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(7) p *::text')
            loader.add_css('basic_insurance', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(13) p *::text')
            yield loader.load_item()
        elif response.url.endswith('inquiryInsuredPerson'):
            data_list: list[dict] = json.loads(response.css('main script[type="text/javascript"]').re(r'\[.*\]')[0])
            for item in data_list:
                loader = AtiehInsuranceItemLoader(selector=response.selector)
                loader.add_value('insurer', item['policyHolder'])
                loader.add_value('fullname', item['insuredName'])
                loader.add_value('birthdate', item['birthDate'])
                loader.add_value('father_name', item['fatherName'])
                loader.add_value('relationship', item['relationName'])
                loader.add_value('national_code', item['nationalCode'])
                loader.add_value('customer_group', item['personGroupName'])
                loader.add_value('end_date', item['startDate'])
                loader.add_value('start_date', item['endDate'])
                loader.add_value('insurance_name', item['insurerCompany'])
                loader.add_value('basic_insurance', item['firstInsurerCompany'])
                yield loader.load_item()
        else:
            return None
