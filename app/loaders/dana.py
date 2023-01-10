# Core imports.
from itemloaders import ItemLoader
from itemloaders.processors import Join, MapCompose

# Local imports.
from app.items.dana import DanaInsuranceItem


__all__ = ('DanaInsuranceItemLoader',)


class DanaInsuranceItemLoader(ItemLoader):
    default_item_class = DanaInsuranceItem
    default_input_processor = MapCompose(str)
    default_output_processor = Join()
