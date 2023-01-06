# Standard imports
import re


def to_snake_case(name) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
