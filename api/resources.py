# Core imports.
from scrapy.utils.misc import load_object

# Third-party imports.
from scrapyrt.conf import app_settings
from scrapyrt.utils import extract_scrapy_request_args
from twisted.internet import defer
from scrapyrt.resources import CrawlResource as DefaultCrawlResource
from twisted.web.server import Request as TwistedRequest


class BaseCrawlResource(DefaultCrawlResource):
    allowedMethods: list[str] = ['GET']
    load_stats: bool = getattr(app_settings, 'LOAD_STATS', False)
    load_items_dropped: bool = getattr(app_settings, 'ITEMS_DROPPED', False)

    def render_GET(self, request: TwistedRequest, **kwargs: None) -> defer:
        api_params = dict((name.decode('utf-8'), value[0].decode('utf-8')) for name, value in request.args.items())
        national_code = request.args.get(b'national_code', [b''])[0].decode()
        api_params.update({'start_requests': True, 'crawl_args': {'national_code': national_code}})
        scrapy_request_args = extract_scrapy_request_args(api_params, raise_error=False)
        return self.prepare_crawl(api_params, scrapy_request_args, **kwargs)

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


class BasicInsuranceCrawlResource(BaseCrawlResource):
    def run_crawl(
        self,
        spider_name,
        scrapy_request_args,
        max_requests=None,
        crawl_args=None,
        start_requests=False,
        *args,
        **kwargs,
    ):
        crawl_manager_cls = load_object(app_settings.CRAWL_MANAGER)
        manager = crawl_manager_cls(
            spider_name,
            scrapy_request_args,
            max_requests,
            start_requests=start_requests,
            spider_module_path='app.spiders.basic',
        )
        if crawl_args:
            kwargs.update(crawl_args)
        dfd = manager.crawl(*args, **kwargs)
        return dfd


class SupplementalInsuranceInsuranceCrawlResource(BaseCrawlResource):
    def run_crawl(
        self,
        spider_name,
        scrapy_request_args,
        max_requests=None,
        crawl_args=None,
        start_requests=False,
        *args,
        **kwargs,
    ):
        crawl_manager_cls = load_object(app_settings.CRAWL_MANAGER)
        manager = crawl_manager_cls(
            spider_name,
            scrapy_request_args,
            max_requests,
            start_requests=start_requests,
            spider_module_path='app.spiders.supplemental',
        )
        if crawl_args:
            kwargs.update(crawl_args)
        dfd = manager.crawl(*args, **kwargs)
        return dfd
