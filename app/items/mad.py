# Standard imports
from dataclasses import dataclass


__all__ = ('MadInsuranceItem',)


@dataclass
class MadInsuranceItem:
    support: str = str()
    end_date: str = str()
    start_date: str = str()
    relationship: str = str()
    national_code: str = str()
    customer_name: str = str()
