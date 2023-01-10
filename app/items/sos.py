# Core imports.
from scrapy import Item, Field


__all__ = ('SosInsuranceItem',)


class SosInsuranceItem(Item):
    end_date = Field()
    last_name = Field()
    first_name = Field()
    start_date = Field()
    contract_name = Field()
    insurance_name = Field()
