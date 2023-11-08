from flask import jsonify

def get_watchlist_by_user_id(user_id, connection):    
    with connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                               SELECT film_id, is_watched, created_at, backdrop_path, title, vote_average 
                               FROM watchlist
                               JOIN films ON watchlist.film_id = films.id 
                               WHERE watchlist.user_id = (%s);
                               ''', (user_id,))
                result = cursor.fetchall()
                column_names = cursor.description
                column_names = [desc[0] for desc in cursor.description]

    watchlist = [dict(zip(column_names, row)) for row in result]
    return jsonify({'watchlist': watchlist})  