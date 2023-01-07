# Core imports.
from scrapy.http import Request as ScrapyRequest


__all__ = ('disable_cache',)


def _append_disable_cache_meta(request_item):
    if isinstance(request_item, ScrapyRequest):
        request_item.meta['dont_cache'] = True
    return request_item


def disable_cache(func):
    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        try:
            for item in resp:
                yield _append_disable_cache_meta(item)
        except TypeError:
            yield _append_disable_cache_meta(resp)

    return wrapper
