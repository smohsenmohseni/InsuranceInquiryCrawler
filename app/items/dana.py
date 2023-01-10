# Core imports.
from scrapy import Item, Field


__all__ = ('DanaInsuranceItem',)


class DanaInsuranceItem(Item):
    gender = Field()
    fullname = Field()
    end_date = Field()
    last_name = Field()
    begin_date = Field()
    first_name = Field()
    birth_year = Field()
    father_name = Field()
    relationship = Field()
    national_code = Field()
