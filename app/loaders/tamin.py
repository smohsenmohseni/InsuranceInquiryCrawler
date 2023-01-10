# Core imports.
from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst

# Local imports.
from app.items.tamin import TaminInsuranceItem


__all__ = ('TaminInsuranceItemLoader',)


class TaminInsuranceItemLoader(ItemLoader):
    default_item_class = TaminInsuranceItem
    default_output_processor = TakeFirst()
