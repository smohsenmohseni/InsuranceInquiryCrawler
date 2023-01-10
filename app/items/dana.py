# Standard imports
from dataclasses import dataclass


__all__ = ('DanaInsuranceItem',)


@dataclass
class DanaInsuranceItem:
    gender: str = str()
    fullname: str = str()
    end_date: str = str()
    last_name: str = str()
    begin_date: str = str()
    first_name: str = str()
    birth_year: str = str()
    father_name: str = str()
    relationship: str = str()
    national_code: str = str()
