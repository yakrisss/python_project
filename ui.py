"""
Module ui.py

User interface functions for movie search application.
"""

import settings
import table
from logger import get_logger


def show_menu():
    """
    Display the main menu and get user choice.

    Returns:
        int: Selected menu option (0, 1, or 2).
    """
    prompt = """
        Menu:
        1. Search movies
        2. Top 5 most popular queries
        0. Exit
        Select a menu option (1, 2, or 0):
    """
    return get_choice(prompt, [0, 1, 2])


def show_menu_movies():
    """
    Display the movie search menu and get user choice.

    Returns:
        int: Selected menu option (0, 1, 2, 3, or 4).
    """
    prompt = """
        Menu:
        1. Search movie by title
        2. Search movie by actors
        3. Search movie by description
        4. Search movie by genre and release year
        0. Exit
        Select a menu option (1, 2, 3, 4 or 0): 
    """
    return get_choice(prompt, [0, 1, 2, 3, 4])


def get_choice(prompt, choices) -> int:
    """
    Prompt the user to enter a valid choice from a list of options.

    Args:
        prompt (str): The input prompt message.
        choices (list[int]): List of valid integer choices.

    Returns:
        int: The user's validated choice.
    """
    while True:
        try:
            choice = int(input(prompt))
            if choice in choices:
                return choice
            print(f"Please enter one of the following numbers: {', '.join(map(str, choices))}")
        except ValueError:
            print("Invalid input. Please enter a number.")


def film_name() -> str:
    """
    Prompt user to enter a movie title or part of it.

    Returns:
        str: User input converted to lowercase and stripped of leading/trailing spaces.
    """
    return input("Enter the title of the movie or part of it: ").strip().lower()


def actor_name() -> str:
    """
    Prompt user to enter an actor or actress name (full or partial).

    Returns:
        str: User input converted to lowercase and stripped of leading/trailing spaces.
    """
    return input("Enter full or partial name of actor or actress: ").strip().lower()


def description_text() -> str:
    """
    Prompt user to enter a keyword from the movie description.

    Returns:
        str: User input converted to lowercase and stripped of leading/trailing spaces.
    """
    return input("Enter keyword from description: ").strip().lower()


def genre_name() -> str:
    """
    Prompt user to enter a movie genre.

    Returns:
        str: User input converted to lowercase and stripped of leading/trailing spaces.
    """
    return input("Enter the genre: ").strip().lower()


def input_year(prompt) -> int:
    """
    Prompt user to enter a valid year (integer).

    Args:
        prompt (str): The input prompt message.

    Returns:
        int: Validated year entered by the user.
    """
    while True:
        try:
            year = int(input(prompt).strip())
            return year
        except ValueError:
            print("Invalid input. Please enter a valid year (numbers only).")


def min_year() -> int:
    """
    Prompt user to enter the minimum release year.

    Returns:
        int: Validated minimum year.
    """
    return input_year("Enter the minimum release year: ")


def max_year() -> int:
    """
    Prompt user to enter the maximum release year.

    Returns:
        int: Validated maximum year.
    """
    return input_year("Enter the maximum release year: ")

#пагинация - разбивание большого обьема данных на части, часть оптимизации
def paginate_query(search_func, *args):
    """
    Perform paginated querying and show results in chunks.

    Args:
        search_func (callable): Search function that accepts arguments and an offset.
        *args: Arguments for the search function excluding offset.

    Behavior:
        Fetches results in batches defined by settings.MOVIE_RESULT_LIMIT,
        displays them, and asks the user whether to fetch more results.

    Returns:
        None
    """
    offset = 0
    while True:
        data = search_func(*args, offset)
        if not data:
            print("No results")
            break

        table.show_results(data) # функция печати, чтоб облегчить написание в main
        if len(data) < settings.MOVIE_RESULT_LIMIT:
            print("End of results.")
            break
        more = input("Show next 10? (yes/no): ").strip().lower()
        if more != 'yes':
            break
        offset += settings.MOVIE_RESULT_LIMIT
