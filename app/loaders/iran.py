# Core imports.
from itemloaders import ItemLoader
from itemloaders.processors import Join, Compose, MapCompose

# Local imports.
from app.items.iran import IranInsuranceItem
from app.helpers.processors import Strip


__all__ = ('IranInsuranceItemLoader',)


class IranInsuranceItemLoader(ItemLoader):
    default_item_class = IranInsuranceItem
    default_input_processor = MapCompose(str)
    default_output_processor = Compose(Join(), Strip())
