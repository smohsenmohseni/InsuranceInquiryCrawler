# Standard imports
import os

# Core imports.
from scrapy.http import Request
from scrapy.extensions.httpcache import (
    FilesystemCacheStorage as DefaultFilesystemCacheStorage,
)

# Local imports.
from app.generics import GenericSpider


class FilesystemCacheStorage(DefaultFilesystemCacheStorage):
    def _get_request_path(self, spider: GenericSpider, request: Request) -> str:
        key = self._fingerprinter.fingerprint(request).hex()
        return os.path.join(self.cachedir, spider.name(), key[0:2], key)
