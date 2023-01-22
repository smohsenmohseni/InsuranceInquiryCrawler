# Standard imports
import json
from typing import Optional

# Core imports.
from scrapy.http import JsonRequest, TextResponse

# Third-party imports.
from jdatetime import datetime

# Local imports.
from core.typing import GeneratorWithoutSendReturn
from app.generics import GenericSpider
from app.loaders.sos import SosInsuranceItemLoader


class SosInsuranceSpider(GenericSpider):
    franchise_url: str
    person_info_url: str
    remaining_ceiling_url: str

    def start_requests(self) -> GeneratorWithoutSendReturn[JsonRequest]:
        yield JsonRequest(
            self.inquiry_url,
            data={
                'serviceDate': datetime.now().strftime('%Y/%m/%d'),
                'nationalcode': self.national_code,
                'hospitalId': '153398',
            },
            callback=self.franchise_request,
        )

    def franchise_request(self, response: TextResponse) -> GeneratorWithoutSendReturn[JsonRequest]:
        response_model: list[dict] = json.loads(response.body.decode()).get('model')
        for item in response_model:
            loader = SosInsuranceItemLoader()
            self.extract_data(item, loader)
            yield JsonRequest(
                self.franchise_url,
                data={
                    "serviceDate": datetime.now().strftime('%Y/%m/%d'),
                    "contractName": loader.get_output_value('contract_name'),
                    "contractId": loader.get_output_value('contract_id'),
                    "planId": loader.get_output_value('plan_id'),
                    "nationalcode": self.national_code,
                    "hospitalId": "153398",
                    "username": "153398",
                },
                callback=self.remaining_ceiling_request,
                cb_kwargs={'loader': loader},
            )

    def remaining_ceiling_request(
        self, response: TextResponse, loader: SosInsuranceItemLoader
    ) -> GeneratorWithoutSendReturn[JsonRequest]:
        response_model: list[dict] = json.loads(response.body.decode()).get('model')
        for item in response_model:
            self.extract_data(item, loader)
            yield JsonRequest(
                self.remaining_ceiling_url,
                data={
                    "serviceDate": datetime.now().strftime('%Y/%m/%d'),
                    "contractName": loader.get_output_value('contract_name'),
                    "contractId": loader.get_output_value('contract_id'),
                    "planId": loader.get_output_value('plan_id'),
                    "nationalcode": self.national_code,
                    "serviceId": item['diseaseId'],
                    "hospitalId": "153398",
                    "username": "153398",
                    "userId": 38193,
                },
                cb_kwargs={'loader': loader},
                callback=self.parse,
            )

    def parse(self, response: TextResponse, **kwargs: SosInsuranceItemLoader) -> Optional[dict]:
        loader: SosInsuranceItemLoader = kwargs['loader']
        item: dict = json.loads(response.body.decode()).get('model')
        self.extract_data(item, loader)
        return loader.load_item()

    @staticmethod
    def extract_data(item: dict, loader: SosInsuranceItemLoader) -> None:
        loader.add_value('plan_id', item.get('planId'))
        loader.add_value('end_date', item.get('endDate'))
        loader.add_value('last_name', item.get('lastName'))
        loader.add_value('franchise', item.get('franchize'))
        loader.add_value('first_name', item.get('firstName'))
        loader.add_value('start_date', item.get('startDate'))
        loader.add_value('contract_id', item.get('contractId'))
        loader.add_value('disease_name', item.get('diseaseName'))
        loader.add_value('contract_name', item.get('contractName'))
        loader.add_value('insurance_name', item.get('insuranceName'))
        loader.add_value('remaining_ceiling', item.get('max_coverage'))
