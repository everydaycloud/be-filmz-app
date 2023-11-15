from flask import jsonify

def add_review_by_film_id(data, film_id, connection):

    INSERT_NEW_REVIEW = "INSERT INTO reviews (user_id, film_id, original_title, body, rating) VALUES (%s, %s, %s, %s, %s) RETURNING user_id, film_id, original_title, created_at, rating, body;"
    
    user_id = data[ "user_id"]
    original_title = data["original_title"]
    body = data["body"]
    rating = data["rating"]
    with connection: 
        with connection.cursor() as cursor:
                cursor.execute(INSERT_NEW_REVIEW, (user_id, film_id, original_title, body, rating))
                
                new_review = cursor.fetchone()

                connection.commit()

                response_data = {
            "message": "New review added", 
            "user_id": new_review[0],
            "film_id": new_review[1],
            "original_title": new_review[2],
            "created_at": new_review[3],
            "rating": new_review[4],
            "body": new_review[5]
            }

        return response_data

      