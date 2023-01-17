# Third-party imports.
from twisted.web.error import Error


__all__ = ('BadRequestException', 'NotFoundException')


class BaseError(Error):
    def __init__(self, message: str) -> None:
        self.message: bytes = bytes(message.encode())


class BadRequestException(BaseError):
    status: bytes = b'400'


class NotFoundException(BaseError):
    status: bytes = b'404'
