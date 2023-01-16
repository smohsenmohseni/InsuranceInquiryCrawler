# Core imports.
from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst, Compose, Join

# Local imports.
from app.items.atieh import AtiehInsuranceItem


__all__ = ('AtiehInsuranceItemLoader',)


class AtiehInsuranceItemLoader(ItemLoader):
    default_item_class = AtiehInsuranceItem
    default_output_processor = TakeFirst()

    remaining_ceiling_out = Compose(Join(), str.strip)
