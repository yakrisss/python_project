import pymysql
import settings
import sql_queries
import mongo_log


class MovieDB:
    def __init__(self):
        self.connection = settings.connection
        self.limit = settings.MOVIE_RESULT_LIMIT

    def query(self, query, params=None):
        with self.connection.cursor() as cursor:
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Ошибка выполнения запроса: {e}")
                return []
    
    def search_film_by_name(self, film_name, offset=0):
        if offset == 0:
            mongo_log.log_create("search_by_name", film_name)
        param = f"%{film_name}%"
        query = sql_queries.QUERY_FILM_BY_NAME
        return self.query(query, (param, self.limit, offset))

    def search_film_by_actor(self, actor_name, offset=0):
        if offset == 0:
            mongo_log.log_create("search_by_actor", actor_name)
        param = f"%{actor_name}%"
        query = sql_queries.QUERY_FILM_BY_ACTOR
        return self.query(query, (param, self.limit, offset))

    def search_film_by_description(self, description_text, offset=0):
        if offset == 0:
            mongo_log.log_create("search_by_description", description_text)
        param = f"%{description_text}%"
        query = sql_queries.QUERY_FILM_BY_DESCRIPTION
        return self.query(query, (param, self.limit, offset))

    def search_film_by_genre_and_year(self, genre, year_min, year_max, offset=0):
        if offset == 0:
            mongo_log.log_create("search_by_genre_and_year", f"{genre} {year_min}-{year_max}")
        param = f"%{genre}%"
        query = sql_queries.QUERY_FILM_BY_GENRE_AND_YEAR
        return self.query(query, (param, year_min, year_max, self.limit, offset))

    def query_all_genres(self):
        query = sql_queries.QUERY_ALL_GENRES
        result = self.query(query)
        return {row[0].lower(): row[0] for row in result}

    def query_min_max_year(self):
        query = sql_queries.QUERY_MIN_MAX_YEAR
        result = self.query(query)
        return result[0] if result else (None, None)
