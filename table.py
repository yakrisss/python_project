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
    """
    headers = ["ID", "Title", "Year", "Genre", "Actors", "Price", "Description"]
    widths = [5, 20, 7, 12, 30, 8, 38]
    header_line = ""
    for h, w in zip(headers, widths):
        header_line += h.ljust(w) + " "
    print(header_line)
    print("-" * len(header_line))

    for row in data:
        wrapped_cols = [
            textwrap.wrap(str(row[i]), width=w) or [''] for i, w in enumerate(widths)
        ]

        max_lines = max(len(col) for col in wrapped_cols)

        for i in range(max_lines):
            line = ""
            for col, w in zip(wrapped_cols, widths):
                cell = col[i] if i < len(col) else ''
                line += cell.ljust(w) + " "
            print(line)


def print_top_searches(data: List[Dict[str, Any]]) -> None:
    """
    Prints a ranked list of the most frequent search queries.

    If the list is empty, prints "No queries found."

    Args:
        data (List[Dict[str, Any]]): List of dictionaries containing search query info.
            Each dictionary should have a key '_id' which is a dict with keys
            'query_type' and 'query_str', and a key 'count' with the number of queries.
    """
    if not data:
        print("No queries found.")
        return
    print("\n")
    for i, item in enumerate(data, start=1):
        _id = item.get('_id', {})
        query_type = _id.get('query_type', 'unknown')
        query_str = _id.get('query_str', '')
        count = item.get('count', 0)
        time_word = 'times' if count != 1 else 'time'
        print(f"{i}. Query - {query_type} by keyword: {query_str} - {count} {time_word}")
