"""
Module ui.py

User interface functions for movie search application.
"""

from typing import List, Callable, Any

import settings # application configuration and DB connection settings
import table
from logger import get_logger # custom logging utility
from exceptions import UserExit


logger = get_logger(__name__)


def show_menu() -> int:
    """
    Display the main menu and get user choice.

    Returns:
        int: Selected menu option (0, 1, or 2).
    """
    prompt = """
        MENU:
        1. Search movies
        2. Top 5 most popular queries
        0. Exit
        Select a menu option (1, 2, or 0):
    """
    return get_choice(prompt, [0, 1, 2])


def show_menu_movies() -> int:
    """
    Display the movie search menu and get user choice.

    Returns:
        int: Selected menu option (0, 1, 2, 3, or 4).
    """
    prompt = """
        MENU:
        1. Search movie by title
        2. Search movie by actors
        3. Search movie by description
        4. Search movie by genre and release year
        0. Exit
        Select a menu option (1, 2, 3, 4 or 0): 
    """
    return get_choice(prompt, [0, 1, 2, 3, 4])


def get_choice(prompt: str, choices: List[int]) -> int:
    """
    Prompt the user to enter a valid choice from a list of options.

    Args:
        prompt (str): The input prompt message.
        choices (List[int]): List of valid integer choices.

    Returns:
        int: The user's validated choice.
    """
    while True:
        try:
            choice = int(input(prompt))
            if choice in choices:
                logger.info("User selected menu option: %s", choice)
                return choice
            print(f"Please enter one of the following numbers: {', '.join(map(str, choices))}")
        except ValueError:
            print("Invalid input. Please enter a number.")


def input_text(prompt: str) -> str:
    """
    Prompt the user to input text, strip it, and convert to lowercase.

    Args:
        prompt (str): The input prompt message.

    Raises:
        UserExit: If the user inputs '0'.

    Returns:
        str: The user's input text.
    """
    value = input(prompt).strip().lower()
    logger.info("User input: '%s' for prompt: '%s'", value, prompt)
    if value == '0':
        raise UserExit()
    return value


def film_name() -> str:
    """Prompt for movie title or part of it."""
    return input_text(
        "Enter the title of the movie or part of it (or 0 for back to previous menu): "
    )


def actor_name() -> str:
    """Prompt for actor name or part of it."""
    return input_text(
    "Enter full or partial name of actor or actress "
    "(or 0 for back to previous menu): "
)


def description_text() -> str:
    """Prompt for description."""
    return input_text("Enter keyword from description (or 0 for back to previous menu): ")


def genre_name() -> str:
    """Prompt for genre."""
    return input_text("Enter the genre (or 0 for back to previous menu): ")


def input_year(prompt: str) -> int:
    """
    Prompt user to enter a valid year (integer).
    """
    while True:
        value = input(f"{prompt} (or 0 for back to previous menu): ").strip()
        if value == '0':
            raise UserExit
        try:
            year = int(value)
            logger.info("User entered year: %d for prompt: %s", year, prompt)
            return year
        except ValueError:
            print("Invalid input. Please enter a valid year (numbers only).")


def prompt_year_range(year_min: int, year_max: int) -> tuple[int, int]:
    """
    Prompt user to input valid min and max year in the given range.

    Args:
        year_min (int): The minimum valid year.
        year_max (int): The maximum valid year.

    Returns:
        tuple[int, int]: A tuple (min_year, max_year) within the specified range
    """
    while True:
        min_y = input_year(f"Enter the minimum release year (from {year_min}): ")
        max_y = input_year(f"Enter the maximum release year (up to {year_max}): ")
        if year_min <= min_y <= max_y <= year_max:
            return min_y, max_y
        invalid_year_range_message(year_min, year_max)


def paginate_query(search_func: Callable[..., List[Any]], *args: Any) -> None:
    """
    Perform paginated querying and show results in chunks.

    Args:
        search_func (callable): Search function that accepts arguments and an offset.
        *args: Arguments for the search function excluding offset.

    Behavior:
        Fetches results in batches defined by settings.MOVIE_RESULT_LIMIT,
        displays them, and asks the user whether to fetch more results.
    """
    offset = 0
    while True:
        data = search_func(*args, offset)
        if not data:
            print("No results")
            break

        table.show_results(data)
        if len(data) < settings.MOVIE_RESULT_LIMIT:
            print("End of results.")
            break
        more = input("Show next 10? (yes or to return to menu no or 0): ").strip().lower()
        if more == 'yes':
            offset += settings.MOVIE_RESULT_LIMIT
        elif more in ('no', '0'):
            print("Returning to the main menu.")
            break
        else:
            print("Invalid input. Returning to the main menu.")
            break

def prompt_genre_choice(genres: dict) -> str:
    """
    Prompt user to enter a genre from the available list.

    Args:
        genres (dict): Dictionary of available genres with {genre_name: id}.

    Raises:
        UserExit: If the user inputs '0'.

    Returns:
        str: The selected genre ID.
    """
    while True:
        show_available_genres(genres)
        genre_input = input_text("Enter the genre (or 0 for back to previous menu): ")
        if genre_input in genres:
            return genres[genre_input]
        invalid_genre_message()


def show_available_genres(genres: dict) -> None:
    """
    Print available genres from dict {genre_name: id}.

    Args:
        genres (dict): Dictionary of available genres..
    """
    print("Available genres:")
    for g in genres:
        print(f" - {g}")


def show_year_range(year_min: int, year_max: int) -> None:
    """
    Print available year range.

    Args:
        year_min (int): Minimum available year.
        year_max (int): Maximum available year.
    """
    print(f"Available release years: from {year_min} to {year_max}")


def show_top_searches(data) -> None:
    """
    Display top 5 most popular queries.

    Args:
        data: Data containing top search queries.
    """
    print("\nTop 5 most popular queries:")
    if not data:
        print("No queries yet.")
    else:
        table.print_top_searches(data)


def invalid_genre_message() -> None:
    """
    Print invalid genre message.
    """
    print("Invalid genre. Please choose from the list.")


def invalid_year_range_message(year_min: int, year_max: int) -> None:
    """
    Print invalid year range message.
    """
    print(f"Error: Please enter years between {year_min} and {year_max}, "
          "and make sure the minimum year is not greater than the maximum year.")
    print("Try again.\n")


def show_message(message: str) -> None:
    """
    General print wrapper for any single message.

    Args:
        message (str): The message to print.
    """
    print(message)
