import settings
import table

def show_menu():
    promt = """
        Menu:
        1. Search movies
        2. Top 5 most popular queries
        0. Exit
        Select a menu option (1, 2, or 0):
    """
    return get_choice(promt, [0, 1, 2])

def show_menu_movies():
    promt = """
        Menu:
        1. Search movie by title
        2. Search movie by actors
        3. Search movie by description
        4. Search movie by genre and release year
        0. Exit
        Select a menu option (1, 2, 3, 4 or 0): 
    """
    return get_choice(promt, [0, 1, 2, 3, 4])

def get_choice(promt, choices):
    while True:
        try:
            choice = int(input(promt))
            if choice in choices:
                return choice
            else:
                print(f"Please enter one of the following numbers: {', '.join(map(str, choices))}")
        except ValueError:
            print("Invalid input. Please enter a number.")

def film_name():
    return input("Enter the title of the movie or part of it: ").strip().lower()

def actor_name():
    return input("Enter full or partial name of actor or actress: ").strip().lower()

def description_text():
    return input("Enter keyword from description: ").strip().lower()

def genre_name():
    return input("Enter the genre: ").strip().lower()

def min_year():
    return int(input("Enter the minimum release year: ").strip())

def max_year():
    return int(input("Enter the maximum release year: ").strip())

def paginate_query(search_func, *args): #сама функция не имеет условия для поиска, имеет функию, к которой обтбор применятес внутри и аргументы
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
