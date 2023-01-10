# Standard imports
from dataclasses import dataclass


__all__ = ('DanaInsuranceItem',)


@dataclass
class DanaInsuranceItem:
    gender: str = ''
    fullname: str = ''
    end_date: str = ''
    last_name: str = ''
    begin_date: str = ''
    first_name: str = ''
    birth_year: str = ''
    father_name: str = ''
    relationship: str = ''
    national_code: str = ''
