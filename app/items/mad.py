# Core imports.
from scrapy import Item, Field


__all__ = ('MadInsuranceItem',)


class MadInsuranceItem(Item):
    support = Field()
    end_date = Field()
    start_date = Field()
    relationship = Field()
    national_code = Field()
    customer_name = Field()
