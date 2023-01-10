# Core imports.
from itemloaders import ItemLoader

# Local imports.
from app.items.tamin import TaminInsuranceItem


__all__ = ('TaminInsuranceItemLoader',)


class TaminInsuranceItemLoader(ItemLoader):
    default_item_class = TaminInsuranceItem
