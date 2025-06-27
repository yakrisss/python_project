import settings

def create_indexes(connection) -> None:
    """
    Creates indexes to optimize film search queries.
    """
    index_queries = [
        # Для фильмов по названию и описанию
        "CREATE INDEX IF NOT EXISTS idx_film_title ON film(title)",
        "CREATE INDEX IF NOT EXISTS idx_film_description ON film(description)",

        # Для фильмов по году выпуска
        "CREATE INDEX IF NOT EXISTS idx_film_release_year ON film(release_year)",

        # Для жанров (category)
        "CREATE INDEX IF NOT EXISTS idx_category_name ON category(name)",

        # Для связи film и category
        "CREATE INDEX IF NOT EXISTS idx_film_category_film_id ON film_category(film_id)",
        "CREATE INDEX IF NOT EXISTS idx_film_category_category_id ON film_category(category_id)",

        # Для связи film и actor
        "CREATE INDEX IF NOT EXISTS idx_film_actor_film_id ON film_actor(film_id)",
        "CREATE INDEX IF NOT EXISTS idx_film_actor_actor_id ON film_actor(actor_id)",

        # Для поиска актёров по имени и фамилии (конкатенация в WHERE — индекс по отдельным полям полезен)
        "CREATE INDEX IF NOT EXISTS idx_actor_first_name ON actor(first_name)",
        "CREATE INDEX IF NOT EXISTS idx_actor_last_name ON actor(last_name)"
    ]

    with connection.cursor() as cursor:
        for query in index_queries:
            try:
                cursor.execute(query)
                print(f"Index created or already exists: {query}")
            except Exception as e:
                print(f"Error creating index: {e}")
    connection.commit()