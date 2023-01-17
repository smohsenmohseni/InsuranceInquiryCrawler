# Core imports.
from itemloaders import ItemLoader
from itemloaders.processors import Join, Compose, MapCompose

# Local imports.
from app.items.mad import MadInsuranceItem


__all__ = ('MadInsuranceItemLoader',)


class MadInsuranceItemLoader(ItemLoader):
    default_item_class = MadInsuranceItem
    default_input_processor = MapCompose(str)
    default_output_processor = Join()

    franchise_out = Compose(Join(), float)
    remaining_ceiling_out = Compose(Join(), float, lambda value: value // 10)
