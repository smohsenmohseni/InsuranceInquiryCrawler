# Core imports.
from itemloaders import ItemLoader
from itemloaders.processors import Join, Compose, MapCompose

# Local imports.
from app.items.iran import IranInsuranceItem


__all__ = ('IranInsuranceItemLoader',)


class IranInsuranceItemLoader(ItemLoader):
    default_item_class = IranInsuranceItem
    default_input_processor = MapCompose(str)
    default_output_processor = Compose(Join(), str.strip)

    franchise_out = Compose(Join(), float)
    remaining_ceiling_out = Compose(Join(), float, lambda value: value // 10)
