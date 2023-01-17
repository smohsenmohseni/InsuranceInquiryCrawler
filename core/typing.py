# Standard imports
from typing import Union, TypeVar, Generator


YieldType = TypeVar('YieldType')


__all__ = (
    'StrIntUnion',
    'GeneratorWithoutSendReturn',
)


StrIntUnion = Union[str, int]
GeneratorWithoutSendReturn = Generator[YieldType, None, None]
