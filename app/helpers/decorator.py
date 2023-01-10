# Standard imports
from typing import Any, Callable, Iterable

# Core imports.
from scrapy.http import Request as ScrapyRequest

# Local imports.
from app.items.common import InvalidInsuranceItem


__all__ = ('disable_cache', 'not_valid_message_if_none')


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


def not_valid_message_if_none(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Iterable[ScrapyRequest] | ScrapyRequest | InvalidInsuranceItem:
        resp: Iterable[ScrapyRequest] | ScrapyRequest | None = func(*args, **kwargs)
        if resp is None:
            return InvalidInsuranceItem()
        return resp

    return wrapper
