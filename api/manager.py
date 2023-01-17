# Third-party imports.
from scrapyrt.core import CrawlManager as DefaultCrawlManager
from scrapyrt.conf.spider_settings import (
    get_project_settings,
    get_scrapyrt_settings,
)


class CrawlManager(DefaultCrawlManager):
    spider_module_path: str

    def __init__(self, *args, **kwargs) -> None:
        self.spider_module_path = kwargs.pop('spider_module_path', '')
        super().__init__(*args, **kwargs)

    def get_project_settings(self):
        # set logfile for a job
        log_file = self._get_log_file_path()
        custom_settings = get_scrapyrt_settings(log_file=log_file)
        if self.spider_module_path:
            custom_settings['SPIDER_MODULES'] = [self.spider_module_path]
        return get_project_settings(custom_settings=custom_settings)
