# Core imports.
from scrapy import Item, Field


__all__ = ('AtiehInsuranceItem',)


class AtiehInsuranceItem(Item):
    insurer = Field()
    end_date = Field()
    fullname = Field()
    birthdate = Field()
    start_date = Field()
    father_name = Field()
    relationship = Field()
    national_code = Field()
    customer_group = Field()
    insurance_name = Field()
    basic_insurance = Field()
