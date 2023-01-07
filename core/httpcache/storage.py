# Standard imports
import os

# Core imports.
from scrapy.extensions.httpcache import (
    FilesystemCacheStorage as BaseFilesystemCacheStorage,
)


class FilesystemCacheStorage(BaseFilesystemCacheStorage):
    def _get_request_path(self, spider, request):
        key = self._fingerprinter.fingerprint(request).hex()
        return os.path.join(self.cachedir, spider.name(), key[0:2], key)
