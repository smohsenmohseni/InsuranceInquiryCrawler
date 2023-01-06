BOT_NAME = 'core'

COMMANDS_MODULE = 'core.commands'
SPIDER_MODULES = ['app.spiders']
NEWSPIDER_MODULE = 'app.spiders'
SPIDER_LOADER_CLASS = 'core.spiderloader.SpiderLoader'

USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
)

REDIRECT_ENABLED = False
RETRY_ENABLED = False

ROBOTSTXT_OBEY = False

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

LOG_ENABLED = True
