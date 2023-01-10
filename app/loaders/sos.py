# Core imports.
from itemloaders import ItemLoader
from itemloaders.processors import Join, MapCompose

# Local imports.
from app.items.sos import SosInsuranceItem


__all__ = ('SosInsuranceItemLoader',)


class SosInsuranceItemLoader(ItemLoader):
    default_item_class = SosInsuranceItem
    default_input_processor = MapCompose(str)
    default_output_processor = Join()
