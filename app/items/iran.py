# Standard imports
from dataclasses import dataclass


__all__ = ('IranInsuranceItem',)


@dataclass
class IranInsuranceItem:
    gender: str = str()
    credit: str = str()
    last_name: str = str()
    birthdate: str = str()
    first_name: str = str()
    start_date: str = str()
    expire_date: str = str()
    father_name: str = str()
