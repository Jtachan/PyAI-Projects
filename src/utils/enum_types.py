"""This module contains extended types to be used at other codes"""
import builtins
import enum


class StrEnum(builtins.str, enum.ReprEnum):
    """Class which elements are strings and is compatible with py <= 3.11"""


class TupleEnum(builtins.tuple, enum.ReprEnum):
    """Class which elements are tuples"""
