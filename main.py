import db
import ui
import mongo_log
import table
from logger import get_logger


def main():
    movie_db = db.MovieDB()

    while True:
        choice = ui.show_menu()

        match choice:
            case 1:
                handle_movie_search(movie_db)

            case 2:
                top_searches = mongo_log.get_top_5_queries(5)
                ui.show_top_searches(top_searches)

            case 0:
                ui.show_message("Exit")
                break

            case _:
                ui.show_message("Invalid choice")


def handle_movie_search(movie_db: db.MovieDB) -> None:
    """
    Handle menu movie search
    """
    movie_choice = ui.show_menu_movies()

    match movie_choice:
        case 1:
            name = ui.film_name()
            ui.paginate_query(movie_db.search_film_by_name, name)

        case 2:
            name = ui.actor_name()
            ui.paginate_query(movie_db.search_film_by_actor, name)

        case 3:
            desc = ui.description_text()
            ui.paginate_query(movie_db.search_film_by_description, desc)

        case 4:
            genres = movie_db.query_all_genres()
            genre = ui.prompt_genre(genres)  

            year_min, year_max = movie_db.query_min_max_year()
            ui.show_year_range(year_min, year_max)

            min_year, max_year = ui.prompt_year_range(year_min, year_max)

            ui.paginate_query(movie_db.search_film_by_genre_and_year, genre, min_year, max_year)

        case 0:
            pass

        case _:
            ui.show_message("Invalid choice in the movie menu")


if __name__ == "__main__":
    main()