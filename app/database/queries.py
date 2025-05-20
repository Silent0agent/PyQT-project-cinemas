GET_SESSIONS = """
SELECT durability, Films.name, price, time_start, places_mat, Sessions.id
FROM Sessions JOIN Films ON Sessions.film_id = Films.id JOIN Halls ON Sessions.hall_id = Halls.id
JOIN Cinemas ON Halls.cinema_id = Cinemas.id
JOIN Places_mats ON Sessions.id = Places_mats.id WHERE Cinemas.name = ?
"""
