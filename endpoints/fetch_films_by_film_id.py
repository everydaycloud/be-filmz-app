def fetch_films_by_film_id(connection, film_id):
    query = """
    SELECT * FROM films
    WHERE id=%s;
    """
    with connection:
        cursor = connection.cursor() 
        cursor.execute(query, (film_id,))
        films = cursor.fetchall()
        if films:
            result = []
            for film in films:
                result.append({
                    "id": film[3],
                    "original_title": film[5],
                    "overview": film[6],
                    "poster_path": film[8],
                    "release_date": film[9],
                    "vote_average": film[12],
                    "vote_count": film[13]
                })
        cursor.close()
    return result[0]