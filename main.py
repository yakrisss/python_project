"""
Main application module to manage movie search and logging functionality.

- Establishes connections to MySQL and MongoDB databases on startup.
- Provides a command-line user interface (UI) for interacting with the movie database.
- Allows searching movies by various criteria: name, actor, description, genre/year.
- Displays top 5 popular search queries from MongoDB logs.
- Handles graceful exits, resource cleanup, and logs errors/information.
"""


import settings  # application configuration and DB connection settings
import db        # database abstraction layer (MovieDB class)
import ui        # user interface functions for input/output
import logger    # custom logging utility
import mongo_log # functions to log search activity into MongoDB


logger = logger.get_logger(__name__)


def main() -> None:
    """
    Main entry point of the application.

    Establishes database connections, then enters a loop displaying the main menu.
    Handles user choices to search movies or view top searches.
    Manages cleanup of database connections on exit or error.
    """
    mysql_conn = settings.mysql_connection
    if not mysql_conn or not mysql_conn.open:
        ui.show_message("MySQL connection is not available.")
        logger.error("MySQL connection is not available.")
        return

    mysql_cursor = None
    try:
        mysql_cursor = mysql_conn.cursor()
    except Exception as e:
        ui.show_message(f"Failed to get MySQL cursor: {e}")
        logger.error(f"Failed to get MySQL cursor: {e}")
        return

    mongo_client = settings.mongo_client
    mongo_collection = settings.mongo_collection
    if mongo_client is None or mongo_collection is None:
        ui.show_message("MongoDB connection or collection is not available.")
        logger.error("MongoDB connection or collection is not available.")
        if mysql_cursor is not None:
            mysql_cursor.close()
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
                    except ui.UserExit:
                        ui.show_message("Returning to main menu...")

                case 2:
                    top_searches = mongo_log.get_top_5_queries(5)
                    ui.show_top_searches(top_searches)

                case 0:
                    ui.show_message("Goodbye")
                    break

                case _:
                    ui.show_message("Invalid choice")

    except Exception as e:
        ui.show_message(f"Unexpected error: {e}")
        logger.error(f"Unexpected error: {e}")
        
    finally:
        # Ensure all connections are closed properly on exit
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

    Allows the user to select different search criteria for movies and 
    executes the corresponding search query with pagination.

    Args:
        movie_db (db.MovieDB): The MovieDB instance for querying the database.

    Returns:
        None

    Raises:
        ui.UserExit: If the user opts to exit from the search input.
    """
    movie_choice = ui.show_menu_movies()

    try:
        match movie_choice:
            case 1:
                name = ui.film_name()
                if name is None:
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
        return

if __name__ == "__main__":
    main()
    