# Core imports.
from scrapy.spiderloader import SpiderLoader as DefaultSpiderLoader
from scrapy.utils.spider import iter_spider_classes


class SpiderLoader(DefaultSpiderLoader):
    def _load_spiders(self, module) -> None:
        for spcls in iter_spider_classes(module):
            sp_name: str = spcls.name()
            self._found[sp_name].append((module.__name__, spcls.__name__))
            self._spiders[sp_name] = spcls
