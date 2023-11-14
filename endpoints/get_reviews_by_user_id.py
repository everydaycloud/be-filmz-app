from flask import jsonify

def get_reviews_by_user_id(user_id, connection): 
    if user_id.isdigit(): 
        with connection:
                with connection.cursor() as cursor:
                    cursor.execute('''
                                SELECT avatar, body, created_at, film_id, rating, review_id, r.user_id, username, original_title
                                FROM reviews as r
                                JOIN users ON r.user_id = users.user_id
                                WHERE r.user_id = (%s);
                                ''', 
                                (user_id,))
                    result = cursor.fetchall()
                    if result:
                        column_names = [desc[0] for desc in cursor.description]
                        reviews = [dict(zip(column_names, row)) for row in result]
                        
                        return jsonify({'reviews': reviews}) 
                    else:
                           return { "message": "This user doesn't exist!"}, 404
    else:
        return {"message": "Invalid ID!"}, 400 