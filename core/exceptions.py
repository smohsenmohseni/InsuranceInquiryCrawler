# Third-party imports.
from twisted.web.error import Error


class BadRequestException(Error):
    status = b'400'

    def __init__(self, message: bytes) -> None:
        self.message = message
