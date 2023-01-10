# Standard imports
from dataclasses import dataclass


__all__ = ('SosInsuranceItem',)


@dataclass
class SosInsuranceItem:
    end_date: str = str()
    last_name: str = str()
    first_name: str = str()
    start_date: str = str()
    contract_name: str = str()
    insurance_name: str = str()
