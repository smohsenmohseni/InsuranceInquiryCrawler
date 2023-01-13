# Third-party imports.
from twisted.web.error import Error


__all__ = ('BadRequestException', 'NotFoundException')


class BaseError(Error):
    def __init__(self, message: str) -> None:
        self.message = bytes(message.encode())


class BadRequestException(BaseError):
    status = b'400'


class NotFoundException(BaseError):
    status = b'404'
