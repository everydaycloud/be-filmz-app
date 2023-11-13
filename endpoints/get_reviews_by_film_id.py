from flask import jsonify

def fetch_reviews_by_film_id(film_id, connection):
    if film_id.isdigit():
        with connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM reviews WHERE film_id = (%s);', (film_id,))
                result = cursor.fetchall()
                if result:
                    column_names = [desc[0] for desc in cursor.description]
                    reviews = [dict(zip(column_names, row)) for row in result]
                    return jsonify({'reviews': reviews})  
                else:
                    return { "message": "This film doesn't exist!"}, 404
    else:
        return{"message": "Invalid ID!"}, 400 