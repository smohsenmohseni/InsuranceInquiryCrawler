# Core imports.
from itemloaders import ItemLoader
from itemloaders.processors import Join, Compose, MapCompose

# Local imports.
from app.items.dana import DanaInsuranceItem
from app.helpers.processors import Strip


__all__ = ('DanaInsuranceItemLoader',)


class DanaInsuranceItemLoader(ItemLoader):
    default_item_class = DanaInsuranceItem
    default_input_processor = MapCompose(str)
    default_output_processor = Compose(Join(), Strip())
