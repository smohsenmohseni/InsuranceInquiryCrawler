# Standard imports
from typing import Any, Callable, Iterable

# Core imports.
from scrapy.http import Request as ScrapyRequest


__all__ = ('disable_cache',)


def _append_disable_cache_meta(request_item: ScrapyRequest) -> ScrapyRequest:
    if isinstance(request_item, ScrapyRequest):
        request_item.meta['dont_cache'] = True
    return request_item


def disable_cache(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Iterable[ScrapyRequest] | ScrapyRequest:
        resp: Iterable[ScrapyRequest] | ScrapyRequest = func(*args, **kwargs)
        try:
            for item in resp:
                yield _append_disable_cache_meta(item)
        except TypeError:
            yield _append_disable_cache_meta(resp)

    return wrapper
