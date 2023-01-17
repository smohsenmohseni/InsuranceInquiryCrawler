# Standard imports
import json
from typing import Optional

# Core imports.
from scrapy.http import Request, TextResponse

# Local imports.
from core.typing import GeneratorWithoutSendReturn
from app.generics import GenericSpider
from app.loaders.tamin import TaminInsuranceItemLoader


class TaminInsuranceSpider(GenericSpider):
    def start_requests(self) -> GeneratorWithoutSendReturn[Request]:
        yield Request(self.inquiry_url.format(national_code=self.national_code), callback=self.parse)

    def parse(self, response: TextResponse, **kwargs: None) -> Optional[dict[str, bool]]:
        result: dict = json.loads(response.body)['data']['result']
        if result:
            loader = TaminInsuranceItemLoader()
            loader.add_value('result', result)
            return loader.load_item()
        return None
