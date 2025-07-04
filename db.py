"""
Module for managing movie database queries.

Provides search methods by name, actor, description, genre, and year,
with query logging and result pagination.
"""


from typing import Optional, Dict, Tuple, List, Any

import pymysql

from logger import get_logger
import settings
import sql_queries
import mongo_log


logger = get_logger(__name__)


class MovieDB:
    """
    Database access layer for movie-related queries.

    Attributes:
        connection (pymysql.connections.Connection): Active MySQL connection.
        cursor (pymysql.cursors.Cursor): Cursor for executing SQL queries.
        limit (int): Max number of results to return per query (pagination limit).
    """

    def __init__(self, conn: pymysql.connections.Connection,
                 cursor: pymysql.cursors.Cursor) -> None:
        """
        Initialize MovieDB with active DB connection and cursor.

        Args:
            conn: MySQL connection instance.
            cursor: Cursor object for executing queries.
        """
        self.connection = conn
        self.cursor = cursor
        self.limit = settings.MOVIE_RESULT_LIMIT
        logger.info("MovieDB initialized with limit=%d", self.limit)

    def query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Tuple]:
        """
        Execute a SQL query with optional parameters and fetch all results.

        Args:
            query: SQL query string with placeholders.
            params: Optional tuple of parameters for query placeholders.

        Returns:
            List of tuples representing rows fetched from the database.
            Returns empty list on error.
        """
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
        except pymysql.MySQLError as e:
            logger.error("Error executing query: %s; Exception: %s", query, e)
            return []

    def search_film_by_name(self, film_name: str, offset: int = 0) -> List[Tuple]:
        """
        Search films by name using LIKE pattern with pagination.

        Args:
            film_name: Partial or full film name to search.
            offset: Number of rows to skip for pagination.

        Returns:
            List of matching film records.
        """
        logger.info("Search film by name: '%s', offset: %d", film_name, offset)
        if offset == 0:
            mongo_log.log_create("search_by_name", film_name)
        param = f"%{film_name}%"
        query = sql_queries.QUERY_FILM_BY_NAME
        return self.query(query, (param, self.limit, offset))

    def search_film_by_actor(self, actor_name: str, offset: int = 0) -> List[Tuple]:
        """
        Search films by actor name with pagination.

        Args:
            actor_name: Partial or full actor name.
            offset: Pagination offset.

        Returns:
            List of films featuring the actor.
        """
        logger.info("Search film by actor: '%s', offset: %d", actor_name, offset)
        if offset == 0:
            mongo_log.log_create("search_by_actor", actor_name)
        param = f"%{actor_name}%"
        query = sql_queries.QUERY_FILM_BY_ACTOR
        return self.query(query, (param, self.limit, offset))

    def search_film_by_description(self, description_text: str, offset: int = 0) -> List[Tuple]:
        """
        Search films by description text.

        Args:
            description_text: Text to match within film descriptions.
            offset: Pagination offset.

        Returns:
            List of matching films.
        """
        logger.info("Search film by description: '%s', offset: %d", description_text, offset)
        if offset == 0:
            mongo_log.log_create("search_by_description", description_text)
        param = f"%{description_text}%"
        query = sql_queries.QUERY_FILM_BY_DESCRIPTION
        return self.query(query, (param, self.limit, offset))

    def search_film_by_genre_and_year(self, genre: str,
        year_min: int,
        year_max: int,
        offset: int = 0
    ) -> List[Tuple]:
        """
        Search films by genre and year range with pagination.

        Args:
            genre: Film genre to search for.
            year_min: Minimum release year.
            year_max: Maximum release year.
            offset: Pagination offset.

        Returns:
            List of films matching criteria.
        """

        logger.info("Search film by genre: '%s', year range: %d-%d, offset: %d",
                    genre, year_min, year_max, offset)
        if offset == 0:
            mongo_log.log_create("search_by_genre_and_year", f"{genre} {year_min}-{year_max}")
        param = f"%{genre}%"
        query = sql_queries.QUERY_FILM_BY_GENRE_AND_YEAR
        return self.query(query, (param, year_min, year_max, self.limit, offset))

    def query_all_genres(self) -> Dict[str, str]:
        """
        Retrieve all genres from the database.

        Returns:
            Dictionary mapping lowercase genre names to their original case.
        """
        logger.info("Query all genres")
        query = sql_queries.QUERY_ALL_GENRES
        result = self.query(query)
        return {row[0].lower(): row[0] for row in result}

    def query_min_max_year(self) -> Tuple[Optional[int], Optional[int]]:
        """
        Retrieve the minimum and maximum release years of films in the database.

        Returns:
            Tuple of (min_year, max_year), or (None, None) if no data.
        """
        logger.info("Query min and max year")
        query = sql_queries.QUERY_MIN_MAX_YEAR
        result = self.query(query)
        return result[0] if result else (None, None)
