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
            extracted_data = self.extract_data(item)
            yield JsonRequest(
                self.franchise_url,
                data={
                    "contractName": extracted_data.get('contract_name'),
                    "serviceDate": datetime.now().strftime('%Y/%m/%d'),
                    "contractId": extracted_data.get('contract_id'),
                    "planId": extracted_data.get('plan_id'),
                    "nationalcode": self.national_code,
                    "hospitalId": "153398",
                    "username": "153398",
                },
                cb_kwargs={'extracted_data': extracted_data},
                callback=self.remaining_ceiling_request,
            )

    def remaining_ceiling_request(
        self, response: TextResponse, extracted_data: dict
    ) -> Optional[GeneratorWithoutSendReturn]:
        response = json.loads(response.body.decode())
        if response['isSuccess']:
            response_model: list[dict] = response.get('model')
            for item in response_model:
                if item['diseaseId'] != 4479:
                    continue
                _extracted_data = self.extract_data(item)
                yield JsonRequest(
                    self.remaining_ceiling_url,
                    data={
                        "contractName": extracted_data.get('contract_name'),
                        "serviceDate": datetime.now().strftime('%Y/%m/%d'),
                        "contractId": extracted_data.get('contract_id'),
                        "planId": extracted_data.get('plan_id'),
                        "nationalcode": self.national_code,
                        "hospitalId": "153398",
                        "username": "153398",
                        "serviceId": 4479,
                        "userId": 38193,
                    },
                    cb_kwargs={'extracted_data': {**extracted_data, **_extracted_data}},
                    callback=self.parse,
                )

    def parse(self, response: TextResponse, **kwargs: dict) -> Optional[dict]:
        extracted_data: dict = kwargs['extracted_data']
        item: dict = json.loads(response.body.decode()).get('model')
        _extracted_data = self.extract_data(item)
        return {**extracted_data, **_extracted_data}

    @staticmethod
    def extract_data(item: dict) -> dict:
        loader = SosInsuranceItemLoader()
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
        return dict(loader.load_item())
