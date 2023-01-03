# Core imports.
import scrapy


class LoginSpider(scrapy.Spider):
    name = 'dlogin'
    start_urls = ['http://localhost:8000/admin/login/']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': '09012223218', 'password': 'mohsn'},
            callback=self.after_login,
            meta={'dont_redirect': True, 'handle_httpstatus_list': [302]},
        )

    def after_login(self, response):
        print(response.headers)
