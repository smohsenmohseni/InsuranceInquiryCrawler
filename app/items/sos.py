# Core imports.
from scrapy import Item, Field


__all__ = ('SosInsuranceItem',)


class SosInsuranceItem(Item):
    plan_id = Field()
    end_date = Field()
    franchise = Field()
    last_name = Field()
    first_name = Field()
    start_date = Field()
    contract_id = Field()
    disease_name = Field()
    contract_name = Field()
    insurance_name = Field()
    remaining_ceiling = Field()
