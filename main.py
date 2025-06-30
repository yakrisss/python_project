import settings
import db
import ui
import logger
import mongo_log
import table
from exceptions import UserExit



logger = logger.get_logger(__name__)


def main():
    mysql_conn = settings.mysql_connection
    if not mysql_conn or not mysql_conn.open:
        ui.show_message("MySQL connection is not available.") #принт ошибки
        logger.error("MySQL connection is not available.")
        return
    
    mysql_cursor = None
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
        if mysql_cursor is not None:
            mysql_cursor.close() #закрыть соединения 
        if mysql_conn is not None and mysql_conn.open:
            mysql_conn.close()
        return


    movie_db = db.MovieDB(mysql_conn, mysql_cursor)

    try:
        while True:
            choice = ui.show_menu()

            match choice:
                case 1:
                    try:
                        handle_movie_search(movie_db)
                    except ui.UserExit:  # ДОБАВЛЕНО: ловим исключение выхода из поиска фильмов
                        ui.show_message("Returning to main menu...")

                case 2:
                    top_searches = mongo_log.get_top_5_queries(5)
                    ui.show_top_searches(top_searches)

                case 0:
                    ui.show_message("Exiting the program")
                    break

                case _:
                    ui.show_message("Invalid choice")

    except Exception as e:
        #неожиданные ошибки внутри цикла
        ui.show_message(f"Unexpected error: {e}")
        logger.error(f"Unexpected error: {e}")
        
    finally:
        #гарантированное закрытие в любом случае
        if mysql_cursor is not None:
            mysql_cursor.close()
        if mysql_conn is not None and mysql_conn.open:
            mysql_conn.close()
        if mongo_client is not None:
            mongo_client.close()
        logger.info("All connections closed.")


def handle_movie_search(movie_db: db.MovieDB) -> None:
    """
    Handle menu for movie search options.
    """
    movie_choice = ui.show_menu_movies()

    try:
        match movie_choice:
            case 1:
                name = ui.film_name()
                if name is None:  #ДОБАВЛЕНО: выход по '0' из input_text
                    raise ui.UserExit()
                ui.paginate_query(movie_db.search_film_by_name, name)

            case 2:
                name = ui.actor_name()
                if name is None:
                    raise ui.UserExit()
                ui.paginate_query(movie_db.search_film_by_actor, name)

            case 3:
                desc = ui.description_text()
                if desc is None:
                    raise ui.UserExit()
                ui.paginate_query(movie_db.search_film_by_description, desc)

            case 4:
                genres = movie_db.query_all_genres()
                genre = ui.prompt_genre_choice(genres)
                if genre is None:
                    raise ui.UserExit()

                year_min, year_max = movie_db.query_min_max_year()
                ui.show_year_range(year_min, year_max)

                min_year, max_year = ui.prompt_year_range(year_min, year_max)
                if min_year is None or max_year is None:
                    raise ui.UserExit()

                ui.paginate_query(movie_db.search_film_by_genre_and_year, genre, min_year, max_year)

    except ui.UserExit:
        ui.show_message("Returning to previous menu...")
        # Возврат в меню поиска фильмов
        return

if __name__ == "__main__":
    main()