# Standard imports
import json

# Core imports.
import scrapy
from scrapy.http import JsonRequest


class Test(scrapy.Spider):
    name = 'dlogin'
    start_urls = ['http://localhost:8000/accounts/token/']

    def start_requests(self):
        data_ = {'username': '09012223218', 'password': 'mohsn'}
        yield JsonRequest(self.start_urls[0], data=data_, callback=self.parse)

    def parse(self, response, **kwargs):
        url_ = 'http://localhost:8000/accounts/'
        body = json.loads(response.body)
        req = JsonRequest(
            url_,
            headers={'Authorization': 'Bearer ' + body['access']},
        )
        print(req.headers)
        yield req

    def parse_list(self, response, **kwargs):
        print(response)
