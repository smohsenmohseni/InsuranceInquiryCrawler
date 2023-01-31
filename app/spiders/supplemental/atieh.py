# Standard imports
import json
from typing import Optional
from http.cookies import SimpleCookie

# Core imports.
from scrapy.http import Request, FormRequest, JsonRequest, TextResponse

# Local imports.
from core.typing import GeneratorWithoutSendReturn
from app.generics import GenericSpider
from app.loaders.atieh import AtiehInsuranceItemLoader
from app.helpers.decorator import disable_cache


class AtiehInsuranceSpider(GenericSpider):
    cost_inquiry_url: str
    inquiry_from_several_policy_url: str
    custom_settings = {'REDIRECT_ENABLED': True, 'HTTPCACHE_ENABLED': False}

    def start_requests(self) -> GeneratorWithoutSendReturn[Request]:
        yield Request(self.login_url, callback=self.login_request)

    def login_request(self, response: TextResponse) -> FormRequest:
        return FormRequest.from_response(
            response,
            formdata=self.login_data,
            callback=self.inquiry_request,
        )

    @staticmethod
    def retrieve_authentication_cookie(cookie: str) -> dict[str, str]:
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

    def client_data_parser(self, response: TextResponse) -> Optional[GeneratorWithoutSendReturn]:
        if response.url.endswith('outpatient'):
            loader = AtiehInsuranceItemLoader(selector=response.selector)
            yield self.cost_inquiry_request(response, loader=loader)
        elif response.url.endswith('inquiryInsuredPerson'):
            data_list: list[dict] = json.loads(response.css('main script[type="text/javascript"]').re(r'\[.*\]')[0])
            yield from self.inquiry_requests_from_several_policy(response, data_list)
        else:
            return None

    def inquiry_requests_from_several_policy(self, response: TextResponse, data_list: list[dict]) -> list[FormRequest]:
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

    def cost_inquiry_request(self, response: TextResponse, **kwargs) -> JsonRequest:
        return JsonRequest(
            cb_kwargs=kwargs,
            callback=self.parse,
            url=self.cost_inquiry_url,
            cookies=self.retrieve_authentication_cookie(response.request.headers.get('Cookie').decode()),
        )

    def parse(self, response: TextResponse, **kwargs) -> GeneratorWithoutSendReturn[dict]:
        loader: AtiehInsuranceItemLoader = kwargs.get('loader', AtiehInsuranceItemLoader())
        add_css = loader.add_css
        add_css('insurer', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(8) p *::text')
        add_css('fullname', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(1) p *::text')
        add_css('birthdate', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(5) p *::text')
        add_css('father_name', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(3) p *::text')
        add_css('relationship', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(4) p *::text')
        add_css('national_code', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(2) p *::text')
        add_css('insurance_name', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(7) p *::text')
        add_css('customer_group', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(11) p *::text')
        add_css('basic_insurance', '#policyInfoPanelBox-collapse div.col-md-4:nth-child(13) p *::text')
        # assign second page tree of response
        loader.selector = response.selector
        add_css = loader.add_css
        add_css('franchise', '#_franchisePercent *::text')
        add_css('remaining_ceiling', '#ceiling_remained_amount *::text')
        yield loader.load_item()
