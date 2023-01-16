# Standard imports
import json
from typing import Any, Generator

# Core imports.
from scrapy.http import FormRequest, TextResponse, JsonRequest

from jdatetime import datetime

# Local imports.
from app.generics import GenericSpider
from app.loaders.mad import MadInsuranceItemLoader


class BaseMadSpider(GenericSpider):
    insurance_id: int
    franchise_url: str
    person_info_url: str
    remaining_ceiling_url: str
    authentication_cookie: dict

    def info_name(self) -> str:
        return 'MAD_INSURANCE_INFO'

    def start_requests(self) -> Generator[FormRequest, None, None]:
        yield FormRequest(
            self.login_url,
            formdata=self.login_data,
            callback=self.inquiry_request,
        )

    def inquiry_request(self, response: TextResponse) -> JsonRequest:
        self.authentication_cookie = json.loads(response.body)
        return JsonRequest(
            self.inquiry_url.format(insurance_id=self.insurance_id, national_code=self.national_code),
            cookies=self.authentication_cookie,
            callback=self.person_info_request,
        )

    def person_info_request(self, response: TextResponse) -> JsonRequest:
        resp: dict = json.loads(response.body)
        data: dict = resp['PreAuthEnabledPolicies'][0]
        loader = MadInsuranceItemLoader()
        loader.add_value('policy_id', data['PolicyId'])
        loader.add_value('support', resp['IsUnderCov'])
        loader.add_value('end_date', data['CovEndDate'])
        loader.add_value('start_date', data['CovBeginDate'])
        loader.add_value('customer_name', data['CustomerName'])
        loader.add_value('relationship', data['RelationTypeText'])
        loader.add_value('insured_person_id', data['InsuredPersonId'])
        loader.add_value('national_code', data['InsuredPersonNationalCode'])
        loader.add_value('health_policy_insured_person_id', data['HealthPolicyInsuredPersonId'])
        return JsonRequest(
            self.person_info_url.format(insurance_id=self.insurance_id, cmn_id=data['InsuredPersonId']),
            cookies=self.authentication_cookie,
            callback=self.franchise_request,
            cb_kwargs={'loader': loader}
        )

    def franchise_request(self, response: TextResponse, loader: MadInsuranceItemLoader) -> JsonRequest:
        resp: dict = json.loads(response.body)
        loader.add_value('name', resp['Name'])
        loader.add_value('mobile', resp['Mobile'])
        loader.add_value('birth_day', resp['BirthDay'])
        loader.add_value('last_name', resp['LastName'])
        loader.add_value('birth_year', resp['BirthYear'])
        loader.add_value('father_name', resp['FatherName'])
        loader.add_value('birth_month', resp['BirthMonth'])
        loader.add_value('gender_text', resp['GenderText'])
        loader.add_value('postal_code', resp['PostalCode'])
        return JsonRequest(
            self.franchise_url,
            cookies=self.authentication_cookie,
            callback=self.remaining_ceiling_request,
            cb_kwargs={'loader': loader},
            data={
                'illnessId': 2302,
                'corpId': self.insurance_id,
                'policyId': loader.get_output_value('policy_id'),
                'receptionDate': datetime.now().strftime('%Y/%m/%d'),
                'healthPolicyInsuredPersonId': loader.get_output_value('health_policy_insured_person_id'),
            },
        )

    def remaining_ceiling_request(self, response: TextResponse, loader: MadInsuranceItemLoader):
        # TODO: get franchise data and pass request
        resp: dict = json.loads(response.body)
        return JsonRequest(
            self.remaining_ceiling_url,
            cookies=self.authentication_cookie,
            cb_kwargs={'loader': loader},
            callback=self.parse,
            data={
                'illnessId': 2302,
                'corpId': self.insurance_id,
                'policyId': loader.get_output_value('policy_id'),
                'receptionDate': datetime.now().strftime('%Y/%m/%d'),
                'insuredPersonId': loader.get_output_value('insured_person_id'),
            },
        )

    @staticmethod
    def parse(response: TextResponse, **kwargs: None) -> dict:
        loader: MadInsuranceItemLoader = kwargs.get('loader', MadInsuranceItemLoader())
        return loader.load_item()


class MadAsiaInsuranceSpider(BaseMadSpider):
    insurance_id = 155


class MadMaInsuranceSpider(BaseMadSpider):
    insurance_id = 150


class MadRaziInsuranceSpider(BaseMadSpider):
    insurance_id = 151


class MadAtiehInsuranceSpider(BaseMadSpider):
    insurance_id = 158


class MadTaavonInsuranceSpider(BaseMadSpider):
    insurance_id = 159


class MadNovinInsuranceSpider(BaseMadSpider):
    insurance_id = 178


class MadMihanInsuranceSpider(BaseMadSpider):
    insurance_id = 155


class MadArmanInsuranceSpider(BaseMadSpider):
    insurance_id = 273


class MadParsianInsuranceSpider(BaseMadSpider):
    insurance_id = 543


class MadAlborzInsuranceSpider(BaseMadSpider):
    insurance_id = 2063


class MadSarmadInsuranceSpider(BaseMadSpider):
    insurance_id = 2498


class MadSinaInsuranceSpider(BaseMadSpider):
    insurance_id = 3025


class MadTejaratNoInsuranceSpider(BaseMadSpider):
    insurance_id = 3539


class MadMoalemInsuranceSpider(BaseMadSpider):
    insurance_id = 5650


class MadKosarInsuranceSpider(BaseMadSpider):
    insurance_id = 19023
