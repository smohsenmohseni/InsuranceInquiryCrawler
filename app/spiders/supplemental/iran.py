# Standard imports
from typing import Optional
from http.cookies import SimpleCookie

# Core imports.
from scrapy.http import Request, FormRequest, TextResponse

# Local imports.
from core.typing import GeneratorWithoutSendReturn
from app.generics import GenericSpider
from app.loaders.iran import IranInsuranceItemLoader


class IranInsuranceSpider(GenericSpider):
    franchise_url: str
    login_cookie: dict[str, str] = {}
    custom_settings = {'REDIRECT_ENABLED': True}

    def start_requests(self) -> GeneratorWithoutSendReturn[Request]:
        yield Request(self.login_url, callback=self.login_request)

    def login_request(self, response: TextResponse) -> FormRequest:
        return FormRequest.from_response(
            response,
            formdata=self.login_data,
            meta={'handle_httpstatus_list': [302]},
            callback=self.set_cookie,
        )

    def set_cookie(self, response: TextResponse) -> Request | FormRequest:
        c: SimpleCookie = SimpleCookie()
        c.load(response.headers.get('Set-Cookie').decode())
        if tgc := c.get('TGC'):
            self.login_cookie.update({'TGC': tgc.value})
        elif jsessionid := c.get('JSESSIONID'):
            self.login_cookie.update({'JSESSIONID': jsessionid.value})
        if response.status == 302:
            return Request(
                response.headers.get('Location').decode(),
                callback=self.set_cookie,
                meta={'handle_httpstatus_list': [302]},
            )
        else:
            return self.inquiry_request(response)

    def inquiry_request(self, response: TextResponse) -> FormRequest:
        return FormRequest.from_response(
            response,
            cookies=self.login_cookie,
            formdata={
                'nationalCode': self.national_code,
                'serviceFlow': 'outpatient',
                '_eventId': 'navigateHcpServicesToFlow',
            },
            clickdata={'id': 'inquiryOutpatientBtn'},
            dont_filter=True,
            callback=self.franchise_request,
        )

    def franchise_request(self, response: TextResponse):
        return FormRequest(
            self.franchise_url,
            cookies=self.login_cookie,
            method='POST',
            formdata={
                'serviceId': '42',
                'showEPrescriptionButton': '',
                'showSaveBtn': 'true',
                '_eventId': '',
            },
            dont_filter=True,
            callback=self.parse,
        )

    def parse(self, response: TextResponse, **kwargs: None) -> Optional[dict]:
        loader = IranInsuranceItemLoader(selector=response.selector)
        self.extract_data(loader)
        return result if (result := loader.load_item()) and all(result.__dict__.values()) else None

    @staticmethod
    def extract_data(loader: IranInsuranceItemLoader) -> None:
        add_css = loader.add_css
        add_css('franchise', '.DemisT2 .base-value-info *::text')
        add_css('remaining_ceiling', '#ceilingRemainedAmount *::text')
        add_css('gender', 'tr:nth-child(2) .DemisT3:nth-child(2) .base-value-info *::text')
        add_css('credit', 'tr:nth-child(3) .DemisT3:nth-child(2) .base-value-info *::text')
        add_css('birthdate', 'tr:nth-child(3) .DemisT3:nth-child(4) .base-value-info *::text')
        add_css('start_date', 'tr:nth-child(4) .DemisT3:nth-child(4) .base-value-info *::text')
        add_css('expire_date', 'tr:nth-child(4) .DemisT3:nth-child(6) .base-value-info *::text')
        add_css('last_name', 'td tr:nth-child(1) .DemisT3:nth-child(4) .base-value-info *::text')
        add_css('first_name', 'td tr:nth-child(1) .DemisT3:nth-child(2) .base-value-info *::text')
        add_css('father_name', 'td tr:nth-child(1) .DemisT3:nth-child(6) .base-value-info *::text')
