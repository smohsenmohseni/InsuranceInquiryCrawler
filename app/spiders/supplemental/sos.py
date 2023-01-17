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
    def start_requests(self) -> GeneratorWithoutSendReturn[JsonRequest]:
        data_: dict[str, str] = {
            'serviceDate': datetime.now().strftime('%Y/%m/%d'),
            'hospitalId': '153398',
            'nationalcode': self.national_code,
        }
        yield JsonRequest(self.inquiry_url, data=data_, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs: None) -> Optional[dict]:
        response_model: list[dict] = json.loads(response.body.decode()).get('model')
        if response_model:
            loader = SosInsuranceItemLoader()
            loader.add_value('end_date', response_model[0]['endDate'])
            loader.add_value('last_name', response_model[0]['lastName'])
            loader.add_value('first_name', response_model[0]['firstName'])
            loader.add_value('start_date', response_model[0]['startDate'])
            loader.add_value('contract_name', response_model[0]['contractName'])
            loader.add_value('insurance_name', response_model[0]['insuranceName'])
            return loader.load_item()
        return None
