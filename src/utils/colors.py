"""
This module contains enums to work with colors
"""
from enum_types import TupleEnum


class BGRColor(TupleEnum):
    """Colors enumeration with BGR encoding"""

    BLUE = (255, 0, 0)
    GREEN = (0, 255, 0)
    RED = (0, 0, 255)
    YELLOW = (0, 255, 255)
    PINK = (255, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
