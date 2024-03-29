# Standard imports
import re


__all__ = ('to_snake_case',)


def to_snake_case(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
