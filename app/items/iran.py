# Core imports.
from scrapy import Item, Field


__all__ = ('IranInsuranceItem',)


class IranInsuranceItem(Item):
    gender = Field()
    credit = Field()
    franchise = Field()
    last_name = Field()
    birthdate = Field()
    first_name = Field()
    start_date = Field()
    expire_date = Field()
    father_name = Field()
    remaining_ceiling = Field()
