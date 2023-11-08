def fetch_films_by_film_id(connection, film_id):
    query=f"""
    SELECT * FROM films
    WHERE id={film_id};
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            films=cursor.fetchall()
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
    return result[0]