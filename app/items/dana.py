# Core imports.
from scrapy import Item, Field


__all__ = ('DanaInsuranceItem',)


class DanaInsuranceItem(Item):
    id = Field()
    gender = Field()
    insured = Field()
    fullname = Field()
    end_date = Field()
    franchise = Field()
    policy_id = Field()
    last_name = Field()
    begin_date = Field()
    first_name = Field()
    birth_year = Field()
    father_name = Field()
    insured_plan = Field()
    relationship = Field()
    national_code = Field()
    policy_type_id = Field()
    remaining_ceiling = Field()
