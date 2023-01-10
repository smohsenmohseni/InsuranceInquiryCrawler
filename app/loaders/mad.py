# Core imports.
from itemloaders import ItemLoader
from itemloaders.processors import Join, MapCompose

# Local imports.
from app.items.mad import MadInsuranceItem


__all__ = ('MadInsuranceItemLoader',)


class MadInsuranceItemLoader(ItemLoader):
    default_item_class = MadInsuranceItem
    default_input_processor = MapCompose(str)
    default_output_processor = Join()
