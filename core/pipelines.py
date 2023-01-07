# Local imports.
from app.generics import GenericSpider


class CorePipeline:
    def process_item(self, item: dict, spider: GenericSpider) -> dict:
        return item
