def fetch_films_by_film_id(connection, film_id):
    query = """
    SELECT
        f.*,
        r.original_title,
        AVG(r.rating) AS average_rating
    FROM
        films f
    JOIN
        reviews r ON f.id = r.film_id
    WHERE
        f.id = %s
    GROUP BY
        f.id, r.original_title;
    """
    if film_id.isdigit():
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
                        "average_rating": film[15]
                    })
                cursor.close()
                return result[0]
            else:
                return { "message": "This film doesn't exist!"}, 404
    else:
        return{"message": "Invalid ID!"}, 400    