# Core imports.
from scrapy import Item, Field


__all__ = ('MadInsuranceItem',)


class MadInsuranceItem(Item):
    name = Field()
    mobile = Field()
    support = Field()
    end_date = Field()
    policy_id = Field()
    last_name = Field()
    franchise = Field()
    birth_day = Field()
    start_date = Field()
    birth_year = Field()
    postal_code = Field()
    gender_text = Field()
    birth_month = Field()
    father_name = Field()
    relationship = Field()
    national_code = Field()
    customer_name = Field()
    insured_person_id = Field()
    remaining_ceiling = Field()
    health_policy_insured_person_id = Field()
