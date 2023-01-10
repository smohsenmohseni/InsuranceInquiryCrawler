# Core imports.
from itemloaders import ItemLoader
from itemloaders.processors import Join, Compose, MapCompose

# Local imports.
from app.items.mad import MadInsuranceItem
from app.helpers.processors import Strip


__all__ = ('MadInsuranceItemLoader',)


class MadInsuranceItemLoader(ItemLoader):
    default_item_class = MadInsuranceItem
    default_input_processor = MapCompose(str)
    default_output_processor = Compose(Join(), Strip())
