QUERY_FILM_BY_NAME = """
SELECT f.film_id, f.title, f.release_year, c.name AS genre,
    GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) ORDER BY a.first_name, a.last_name SEPARATOR ', ') AS actors,
    f.rental_rate, f.description
FROM film AS f
LEFT JOIN film_category AS fc ON f.film_id = fc.film_id
LEFT JOIN category AS c ON fc.category_id = c.category_id
LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
WHERE f.title LIKE %s
GROUP BY f.film_id, f.title, f.release_year, c.name, f.rental_rate, f.description
LIMIT %s OFFSET %s
"""

QUERY_FILM_BY_ACTOR = """
SELECT f.film_id, f.title, f.release_year, c.name AS genre,
    GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) ORDER BY a.first_name, a.last_name SEPARATOR ', ') AS actors,
    f.rental_rate, f.description
FROM film AS f
LEFT JOIN film_category AS fc ON f.film_id = fc.film_id
LEFT JOIN category AS c ON fc.category_id = c.category_id
LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
WHERE CONCAT(a.first_name, ' ', a.last_name) LIKE %s
GROUP BY f.film_id, f.title, f.release_year, c.name, f.rental_rate, f.description
LIMIT %s OFFSET %s
"""

QUERY_FILM_BY_DESCRIPTION = """
SELECT f.film_id, f.title, f.release_year, c.name AS genre,
    GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) ORDER BY a.first_name, a.last_name SEPARATOR ', ') AS actors,
    f.rental_rate, f.description
FROM film AS f
LEFT JOIN film_category AS fc ON f.film_id = fc.film_id
LEFT JOIN category AS c ON fc.category_id = c.category_id
LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
WHERE f.description LIKE %s
GROUP BY f.film_id, f.title, f.release_year, c.name, f.rental_rate, f.description
LIMIT %s OFFSET %s
"""

QUERY_FILM_BY_GENRE_AND_YEAR = """
SELECT f.film_id, f.title, f.release_year, c.name AS genre,
    GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) ORDER BY a.first_name, a.last_name SEPARATOR ', ') AS actors,
    f.rental_rate, f.description
FROM film AS f
LEFT JOIN film_category AS fc ON f.film_id = fc.film_id
LEFT JOIN category AS c ON fc.category_id = c.category_id
LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
WHERE c.name LIKE %s AND f.release_year BETWEEN %s AND %s
GROUP BY f.film_id, f.title, f.release_year, c.name, f.rental_rate, f.description
LIMIT %s OFFSET %s
"""

QUERY_ALL_GENRES = "SELECT DISTINCT name FROM category"

QUERY_MIN_MAX_YEAR = "SELECT MIN(release_year), MAX(release_year) FROM film"