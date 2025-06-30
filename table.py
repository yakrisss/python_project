"""
Module for displaying formatted tabular data and printing search query statistics.

Functions:
- show_results(data: List[List[Any]]) -> None:
    Displays tabular data with automatic text wrapping inside table cells.

- print_top_searches(data: List[Dict[str, Any]]) -> None:
    Prints a ranked list of the most frequent search queries from given data.

This module is useful for formatting console output when working with
search results, reports, or logs that require readable multi-line columns.
"""


import textwrap
from typing import List, Dict, Any


def show_results(data: List[List[Any]]) -> None:
    """
    Display tabular data with wrapped text inside cells.

    Each row is printed with columns aligned and wrapped to the specified width.

    Args:
        data (List[List[Any]]): List of rows, where each row is a list of cell values.

    Returns:
        None
    """
    headers = ["ID", "Title", "Year", "Genre", "Actors", "Price", "Description"]
    widths = [5, 20, 7, 12, 30, 8, 38]
    header_line = ""
    for h, w in zip(headers, widths):
        header_line += h.ljust(w) + " "
    print(header_line)
    print("-" * len(header_line))

    # колонки с переносами, где надо
    for row in data:
        # разбиваю каждую ячейку на строки с переносом
        wrapped_cols = [
            textwrap.wrap(str(row[i]), width=w) or [''] for i, w in enumerate(widths)
        ]

        # максимальное число строк в этом ряду (для переносов)
        max_lines = max(len(col) for col in wrapped_cols)

        # по строкам, чтобы переносить текст в ячейках
        for i in range(max_lines):
            line = ""
            for col, w in zip(wrapped_cols, widths):
                # если в этом столбце есть строка на текущей линии, печатаем или пробелы
                cell = col[i] if i < len(col) else ''
                line += cell.ljust(w) + " "
            print(line)


def print_top_searches(data: List[Dict[str, Any]]) -> None:
    """
    Print the most frequent search queries.

    Args:
        data (List[Dict[str, Any]]): List of dictionaries containing search query info,
            each with keys '_id' and 'count'. '_id' is a dict with 'query_type' and 'query_str'.

    Returns:
        None
    """
    print("Most frequent search queries:")
    for i, item in enumerate(data, start=1):
        _id = item.get('_id', {})
        query_type = _id.get('query_type', 'unknown')
        query_str = _id.get('query_str', '')
        count = item.get('count', 0)
        time_word = 'times' if count != 1 else 'time'
        print(f"{i}. Query - {query_type} by keyword {query_str} - {count} {time_word}")

    