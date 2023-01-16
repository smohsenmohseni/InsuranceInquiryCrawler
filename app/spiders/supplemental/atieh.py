# Standard imports
import json
from typing import Generator
from http.cookies import SimpleCookie

# Core imports.
from scrapy.http import Request, FormRequest, JsonRequest, TextResponse

# Local imports.
from app.generics import GenericSpider
from app.loaders.atieh import AtiehInsuranceItemLoader
from app.helpers.decorator import disable_cache


class AtiehInsuranceSpider(GenericSpider):
    cost_inquiry_url: str
    inquiry_from_several_policy_url: str
    custom_settings = {'REDIRECT_ENABLED': True, 'HTTPCACHE_ENABLED': False}

    def start_requests(self) -> Generator[Request, None, None]:
        yield Request(self.login_url, callback=self.login_request)

    def login_request(self, response: TextResponse) -> FormRequest:
        return FormRequest.from_response(
            response,
            formdata=self.login_data,
            callback=self.inquiry_request,
        )

    @staticmethod
    def retrieve_authentication_cookie(cookie: str) -> dict:
        c: SimpleCookie = SimpleCookie()
        c.load(cookie)
        return {'JSESSIONID': c['JSESSIONID'].value}

    @disable_cache
    def inquiry_request(self, response: TextResponse) -> FormRequest:
        yield FormRequest(
            method='POST',
            callback=self.client_data_parser,
            url=self.inquiry_url,
            cookies=self.retrieve_authentication_cookie(response.request.headers.get('Cookie').decode()),
            formdata={
                'nationalCode': self.national_code,
                'requestType': 'outpatient',
                '_nonav': '',
            },
        )

    def client_data_parser(self, response: TextResponse) -> Generator[dict | Generator, None, None] | None:
        if response.url.endswith('outpatient'):
            loader = AtiehInsuranceItemLoader(selector=response.selector)
            yield self.cost_inquiry_request(response, loader=loader)
        elif response.url.endswith('inquiryInsuredPerson'):
            data_list: list[dict] = json.loads(response.css('main script[type="text/javascript"]').re(r'\[.*\]')[0])
            yield from self.inquiry_requests_from_several_policy(response, data_list)
        else:
            return None

    def inquiry_requests_from_several_policy(self, response: TextResponse, data_list: list) -> list:
        return [
            FormRequest(
                method='POST',
                callback=self.client_data_parser,
                url=self.inquiry_from_several_policy_url,
                cookies=self.retrieve_authentication_cookie(response.request.headers.get('Cookie').decode()),
                dont_filter=True,
                formdata={
                    'requestType': 'outpatient',
                    'policyType': str(policy.get('policyType')),
                    'policyId': str(policy.get('policyId')),
                },
            )
            for policy in data_list
        ]

    def cost_inquiry_request(self, response: TextResponse, **kwargs):
        return JsonRequest(
            cb_kwargs=kwargs,
            callback=self.parse,
            url=self.cost_inquiry_url,
            cookies=self.retrieve_authentication_cookie(response.request.headers.get('Cookie').decode()),
        )

    def parse(self, response: TextResponse, **kwargs) -> Generator[dict, None, None]:
        loader: AtiehInsuranceItemLoader = kwargs.get('loader', AtiehInsuranceItemLoader())
        loader.add_css('insurer', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(8) p *::text')
        loader.add_css('fullname', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(1) p *::text')
        loader.add_css('birthdate', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(5) p *::text')
        loader.add_css('father_name', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(3) p *::text')
        loader.add_css('relationship', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(4) p *::text')
        loader.add_css('national_code', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(2) p *::text')
        loader.add_css('customer_group', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(11) p *::text')
        loader.add_css('insurance_name', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(7) p *::text')
        loader.add_css('basic_insurance', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(13) p *::text')
        loader.selector = response.selector
        loader.add_css('franchise', '#_franchisePercent *::text')
        loader.add_css('remaining_ceiling', '#ceiling_remained_amount *::text')
        yield loader.load_item()
