# Standard imports
from typing import Generator
from http.cookies import SimpleCookie

# Core imports.
from scrapy.http import Request, FormRequest, TextResponse

# Local imports.
from app.generics import GenericSpider


class IranInsuranceSpider(GenericSpider):
    custom_settings: dict[str, bool] = {'REDIRECT_ENABLED': True}
    login_cookie: dict[str, str] = dict()

    def start_requests(self) -> Generator[Request, None, None]:
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
            callback=self.parse,
        )

    def parse(self, response: TextResponse, **kwargs: None) -> dict:
        if not response.url.endswith('e1s1'):
            values: list[str] = response.css('td.DemisT3 span *::text').getall()
            return {
                'first_name': values[0],
                'last_name': values[1],
                'father_name': values[2],
                'gender': values[3],
                'credit': values[6],
                'birthdate': values[7],
                'start_date': values[10],
                'expire_date': values[11],
            }
        return {'status': 'not valid'}
