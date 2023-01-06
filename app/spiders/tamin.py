# Standard imports
import json

# Local imports.
from app.generics import GenericSpider


class TaminInsuranceSpider(GenericSpider):
    def parse(self, response, **kwargs):
        return json.loads(response.body)
