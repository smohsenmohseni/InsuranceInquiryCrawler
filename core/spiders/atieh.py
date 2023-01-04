import re

from scrapy import Spider
from scrapy.http import Request, FormRequest


class AtiehInsuranceSpider(Spider):
    name = 'atieh_insurance'
    login_url = 'https://rasatpa.ir/sso/login?service=https%3A%2F%2Frasatpa.ir%2Fhcp%2Flogin%2Fcas'
    inquiry_url = 'https://rasatpa.ir/hcp/reception/inquiryInsuredPerson'
    custom_settings = {
        'REDIRECT_ENABLED': True,
    }

    def start_requests(self):
        yield Request(self.login_url, dont_filter=True, callback=self.login_request)

    def login_request(self, response):
        return FormRequest.from_response(
            response,
            formdata={
                'username': '44443148',
                'password': 'moein999',
                'execution': 'e1s1',
                '_eventId': 'submit'
            },
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
                'nationalCode': '1930577011',
                'requestType': 'outpatient',
                '_eventId': '',
            },
            meta={'dont_redirect': False,},
            # meta={'dont_redirect': False},
            callback=self.parse,
        )

    def parse(self, response, **kwargs):
        print('\n'*5)
        print('response:', response.url)
        rows = response.css('#insuredList tbody tr')
        for row in rows:
            values = row.css('td *::text').getall()
            yield {
                'name': values[0],
                'insurance': values[2],
                'start_date': values[5],
                'expire_date': values[6],
            }
