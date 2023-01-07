BOT_NAME = 'core'

# Spider
SPIDER_MODULES = ['app.spiders']
NEWSPIDER_MODULE = 'app.spiders'
SPIDER_LOADER_CLASS = 'core.spiderloader.SpiderLoader'

# Commands
COMMANDS_MODULE = 'core.commands'

# User Fingerprint
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
)

# Middlewares
SPIDER_MIDDLEWARES_BASE = {
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
    'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,
    'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,
}
SPIDER_MIDDLEWARES = {}

# Twisted
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

# Logs
LOG_ENABLED = True

# Robots.txt
ROBOTSTXT_OBEY = False

# Http status handlers
RETRY_ENABLED = False
REDIRECT_ENABLED = False

# Cache
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400
HTTPCACHE_IGNORE_HTTP_CODES = [500, 404]
HTTPCACHE_STORAGE = 'core.httpcache.storage.FilesystemCacheStorage'
