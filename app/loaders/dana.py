# Core imports.
from itemloaders import ItemLoader
from itemloaders.processors import Join, Compose, TakeFirst, MapCompose

# Local imports.
from app.items.dana import DanaInsuranceItem


__all__ = ('DanaInsuranceItemLoader',)


class DanaInsuranceItemLoader(ItemLoader):
    default_item_class = DanaInsuranceItem
    default_input_processor = MapCompose(str)
    default_output_processor = Join()

    id_out = TakeFirst()
    franchise_out = Compose(Join(), float)
    remaining_ceiling_out = Compose(Join(), lambda value: value.replace(',', ''), int, lambda value: value // 10)
