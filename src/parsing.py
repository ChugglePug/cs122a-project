# parsing.py

from typing import Any


def format_list(values: list[Any]) -> list[Any]:
    """
    Replaces any 'Null' string values with None
    :param values: list to be formatted
    :return: list with 'Null' replaced with None
    """
    return [None if value.upper() == 'NULL' else value for value in values]
