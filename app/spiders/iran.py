# Standard imports
from http.cookies import SimpleCookie

# Core imports.
from scrapy.http import Request, FormRequest

# Local imports.
from app.generics.base import BaseSpiderGeneric


class IranInsuranceSpider(BaseSpiderGeneric):
    login_url = (
        'https://darman.iraninsurance.ir/dms-cas/'
        'login?service=http%3A%2F%2Fdarman.iraninsurance.ir%2F%2Fj_spring_cas_security_check'
    )
    inquiry_url = 'http://darman.iraninsurance.ir/home-flow?execution=e1s1'
    custom_settings = {
        'REDIRECT_ENABLED': True,
    }
    login_cookie = dict()

    def start_requests(self):
        yield Request(self.login_url, dont_filter=True, callback=self.login_request)

    def login_request(self, response):
        return FormRequest.from_response(
            response,
            formdata={'username': '444431488', 'password': 'moein999'},
            meta={'handle_httpstatus_list': [302]},
            callback=self.set_cookie,
        )

    def set_cookie(self, response):
        c = SimpleCookie()
        c.load(response.headers.get('Set-Cookie').decode())
        if tgc := c.get('TGC'):
            self.login_cookie.update({'TGC': tgc.value})
        elif jsessionid := c.get('JSESSIONID'):
            self.login_cookie.update({'JSESSIONID': jsessionid.value})
        if response.status == 302:
            yield Request(
                response.headers.get('Location').decode(),
                callback=self.set_cookie,
                meta={'handle_httpstatus_list': [302]},
            )
        else:
            yield self.inquiry_request(response)

    def inquiry_request(self, response):
        return FormRequest.from_response(
            response,
            cookies=self.login_cookie,
            formdata={
                'nationalCode': '4172953360',
                'serviceFlow': 'outpatient',
                '_eventId': 'navigateHcpServicesToFlow',
            },
            clickdata={'id': 'inquiryOutpatientBtn'},
            callback=self.parse,
        )

    def parse(self, response, **kwargs):
        values = response.css('td.DemisT3 span *::text').getall()
        yield {
            'first_name': values[0],
            'last_name': values[1],
            'father_name': values[2],
            'gender': values[3],
            'credit': values[6],
            'birthdate': values[7],
            'start_date': values[10],
            'expire_date': values[11],
        }
