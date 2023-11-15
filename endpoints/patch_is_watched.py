from flask import jsonify

def toggle_is_watched(user_id, film_id, connection, is_watched_update):
    
    #Error Handling for this request:
    if not user_id.isdigit():
        return {"message": "Invalid User ID!"}, 400
    
    if not film_id.isdigit():
        return {"message": "Invalid Film ID!"}, 400
    
    user_exists_query= "SELECT * FROM users WHERE user_id = %s;"
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(user_exists_query, (user_id,))
            user_exists = cursor.fetchone()

            if not user_exists:
                return {"message": "This user doesn't exist!"}, 404
            
    film_exists_query= "SELECT * FROM films WHERE id = %s;"
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(film_exists_query, (film_id,))
            user_exists = cursor.fetchone()

            if not user_exists:
                return {"message": "This film doesn't exist!"}, 404        
    
    #PATCH request:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE watchlist
                SET is_watched = %s
                WHERE film_id = %s AND user_id = %s
                RETURNING *;
                """        , 
                (is_watched_update,
                 film_id,
                 user_id))
            updated_watchlist_entry = cursor.fetchone()
            response_data = {
            "user_id": updated_watchlist_entry[0],
            "film_id": updated_watchlist_entry[1],
            "is_watched": updated_watchlist_entry[2],
            "created_at": updated_watchlist_entry[3]
            }
            return jsonify(response_data)  
        
            
    
                

