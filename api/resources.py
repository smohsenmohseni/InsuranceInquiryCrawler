# Third-party imports.
from scrapyrt.conf import app_settings
from scrapyrt.resources import CrawlResource as BaseCrawlResource
from twisted.web.server import Request as TwistedRequest


class CrawlResource(BaseCrawlResource):
    allowedMethods: list[str] = ['GET']
    load_stats: bool = getattr(app_settings, 'LOAD_STATS', False)
    load_items_dropped: bool = getattr(app_settings, 'ITEMS_DROPPED', False)

    def render_GET(self, request: TwistedRequest, **kwargs: None):
        request.args.update({b'start_requests': [b'true']})
        return super().render_GET(request, **kwargs)

    def prepare_response(self, result: dict, *args: None, **kwargs: dict[str, dict]) -> dict:
        items = result.get("items")
        response = {
            "status": "ok",
            "spider_name": result.get("spider_name"),
            "items": items,
        }
        if self.load_stats:
            response["stats"] = result.get("stats")
        if self.load_items_dropped:
            response["items_dropped"] = result.get("items_dropped", [])
        errors = result.get("errors")
        if errors:
            response["errors"] = errors
        return response