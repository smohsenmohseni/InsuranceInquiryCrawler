# Standard imports
from typing import Any

# Core imports.
from scrapy import Spider
from scrapy.http import TextResponse

# Local imports.
from app.constants import info, messages
from core.exceptions import BadRequestException
from app.helpers.transformers import to_snake_case


class GenericSpider(Spider):
    login_url: str
    login_data: dict
    inquiry_url: str
    national_code: str
    custom_settings: dict

    def __init__(self, *args: Any, **kwargs: Any):
        self.__dict__.update(getattr(info, f'{self.name()}_info'.upper(), {}))
        super().__init__(*args, **kwargs)
        self.validations()

    def parse(self, response: TextResponse, **kwargs: None) -> None:
        ...

    def validations(self) -> None:
        """
        :raises BadRequestException: if the national code is not sent, raise 400 request exception
        """
        if not hasattr(self, 'national_code'):
            raise BadRequestException(messages.NATIONAL_CODE_IS_REQUIRED)

    @classmethod
    def name(cls) -> str:
        return to_snake_case(cls.__name__.replace('Spider', ''))
