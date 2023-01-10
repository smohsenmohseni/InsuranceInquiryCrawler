# Core imports.
from scrapy import Item, Field


__all__ = ('TaminInsuranceItem',)


class TaminInsuranceItem(Item):
    result = Field()
