# parsing.py

from typing import Any, Iterable


def format_list(values: Iterable[Any]) -> list[Any]:
    """
    Replaces any 'Null' string values with None
    :param values: list to be formatted
    :return: list with 'Null' replaced with None
    """
    return [None if value.upper() == 'NULL' else value for value in values]


def format_table(values: Iterable[Any]) -> str:
    """
    Returns a comma separated string of values
    :param values: Sequence of non None values that can be cast into a string
    :return: formatted string of values
    """
    return ','.join(['NULL' if e is None else str(e) for e in values])
