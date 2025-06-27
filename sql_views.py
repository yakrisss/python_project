import settings


def create_full_info_film_view(connection):
    view_sql = """
    CREATE OR REPLACE VIEW full_info_film AS
    SELECT 
        f.film_id, 
        f.title, 
        f.description, 
        f.release_year, 
        f.rental_duration, 
        f.rental_rate,
        f.length, 
        f.rating, 
        c.name AS genre,
        GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) ORDER BY a.first_name, a.last_name SEPARATOR ', ') AS actors
    FROM film AS f
    LEFT JOIN film_category AS fc ON f.film_id = fc.film_id
    LEFT JOIN category AS c ON fc.category_id = c.category_id
    LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
    LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
    GROUP BY 
        f.film_id, f.title, f.description, f.release_year, 
        f.rental_duration, f.rental_rate, f.length, f.rating, c.name;
    """
    with connection.cursor() as cursor:
        cursor.execute(view_sql)
    connection.commit()