import settings
import db
import ui
import logger
import mongo_log
import table

logger = logger.get_logger(__name__)


def main():
    mysql_conn = settings.mysql_connection
    if not mysql_conn or not mysql_conn.open:
        ui.show_message("MySQL connection is not available.") #принт ошибки
        logger.error("MySQL connection is not available.")
        return
    
    try:
        mysql_cursor = mysql_conn.cursor()
    except Exception as e:
        ui.show_message(f"Failed to get MySQL cursor: {e}") #принт ошибки
        logger.error(f"Failed to get MySQL cursor: {e}")
        return
    
    mongo_client = settings.mongo_client
    mongo_collection = settings.mongo_collection
    if mongo_client is None or mongo_collection is None:
        ui.show_message("MongoDB connection or collection is not available.")
        logger.error("MongoDB connection or collection is not available.")
        mysql_cursor.close()
        mysql_conn.close() #закрыть соединения sql если нет соединения с монго
        return

    movie_db = db.MovieDB(mysql_conn, mysql_cursor)

    try:
        while True:
            choice = ui.show_menu()

            match choice:
                case 1:
                    handle_movie_search(movie_db)

                case 2:
                    top_searches = mongo_log.get_top_5_queries(5)
                    ui.show_top_searches(top_searches)

                case 0:
                    ui.show_message("Exiting the program")
                    break

                case _:
                    ui.show_message("Invalid choice")

    finally:
        #закрытие соединения поле нажати 0 
        if mysql_cursor is not None:
            mysql_cursor.close()
        if mysql_conn is not None and mysql_conn.open:
            mysql_conn.close()
        if mongo_client is not None:
            mongo_client.close()


def handle_movie_search(movie_db: db.MovieDB) -> None:
    """
    Handle menu for movie search options.
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