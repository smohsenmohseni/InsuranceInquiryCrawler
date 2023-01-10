# Standard imports
from dataclasses import dataclass

# Local imports.
from app.constants import messages


@dataclass
class InvalidInsuranceItem:
    message: str = messages.NOT_VALID_INSURANCE
