# Core imports.
from itemloaders import ItemLoader
from itemloaders.processors import Join, MapCompose, Compose

# Local imports.
from app.items.sos import SosInsuranceItem


__all__ = ('SosInsuranceItemLoader',)


class SosInsuranceItemLoader(ItemLoader):
    default_item_class = SosInsuranceItem
    default_input_processor = MapCompose(str)
    default_output_processor = Join()

    franchise_out = Compose(Join(), float)
    remaining_ceiling_out = Compose(Join(), float, lambda value: value // 10)
