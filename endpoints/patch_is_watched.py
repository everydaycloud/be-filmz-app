# 1. declare toggle_is_watched function
# 2. write SQL query to see if the film is in the user's watchlist
# 3. If it isn't, write another SQL query to post to watchlist, and set
# is_watched to true
# 4. If the film IS in the watchlist, we don't want another SQL query 
# and we will just continue with switching the property to true.
# note: We want to be able to set the property to true or false depending
# on which boolean is in the PATCH request object. 

from .add_new_watchlist_entry import add_new_entry
from flask import jsonify

def toggle_is_watched(user_id, film_id, connection, is_watched_update):
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
        
            
    
                

