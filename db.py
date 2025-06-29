import pymysql
import settings
import sql_queries
import mongo_log
from logger import get_logger

logger = get_logger(__name__)


class MovieDB:
    def __init__(self, conn, cursor):
        self.connection = conn
        self.cursor = cursor
        self.limit = settings.MOVIE_RESULT_LIMIT
        logger.info("MovieDB initialized with limit=%d", self.limit)

    def query(self, query, params=None):
        try:
            if params:
                logger.debug("Executing query: %s with params: %s", query, params)
                self.cursor.execute(query, params)
            else:
                logger.debug("Executing query: %s", query)
                self.cursor.execute(query)
                
            result = self.cursor.fetchall()
            logger.debug("Query executed successfully, fetched %d rows", len(result))
            return result
        except Exception as e:
            logger.error("Error executing query: %s; Exception: %s", query, e)
            return []
    
    def search_film_by_name(self, film_name, offset=0):
        logger.info("Search film by name: '%s', offset: %d", film_name, offset)
        if offset == 0:
            mongo_log.log_create("search_by_name", film_name)
        param = f"%{film_name}%"
        query = sql_queries.QUERY_FILM_BY_NAME
        return self.query(query, (param, self.limit, offset))

    def search_film_by_actor(self, actor_name, offset=0):
        logger.info("Search film by actor: '%s', offset: %d", actor_name, offset)
        if offset == 0:
            mongo_log.log_create("search_by_actor", actor_name)
        param = f"%{actor_name}%"
        query = sql_queries.QUERY_FILM_BY_ACTOR
        return self.query(query, (param, self.limit, offset))

    def search_film_by_description(self, description_text, offset=0):
        logger.info("Search film by description: '%s', offset: %d", description_text, offset)
        if offset == 0:
            mongo_log.log_create("search_by_description", description_text)
        param = f"%{description_text}%"
        query = sql_queries.QUERY_FILM_BY_DESCRIPTION
        return self.query(query, (param, self.limit, offset))

    def search_film_by_genre_and_year(self, genre, year_min, year_max, offset=0):
        logger.info("Search film by genre: '%s', year range: %d-%d, offset: %d", genre, year_min, year_max, offset)
        if offset == 0:
            mongo_log.log_create("search_by_genre_and_year", f"{genre} {year_min}-{year_max}")
        param = f"%{genre}%"
        query = sql_queries.QUERY_FILM_BY_GENRE_AND_YEAR
        return self.query(query, (param, year_min, year_max, self.limit, offset))

    def query_all_genres(self):
        logger.info("Query all genres")
        query = sql_queries.QUERY_ALL_GENRES
        result = self.query(query)
        return {row[0].lower(): row[0] for row in result}

    def query_min_max_year(self):
        logger.info("Query min and max year")
        query = sql_queries.QUERY_MIN_MAX_YEAR
        result = self.query(query)
        return result[0] if result else (None, None)
