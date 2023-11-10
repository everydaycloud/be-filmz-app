from flask import jsonify, abort
import psycopg2

INSERT_NEW_ENTRY = "INSERT INTO watchlist (user_id, film_id) VALUES (%s, %s) RETURNING user_id, film_id, is_watched, created_at;"

def add_new_entry(data, connection, user_id):
    print(data, "log of data")
    film_id = data["film_id"]

    if film_id == None:
         return {'message': 'film_id is required'}, 400
    
    try:
        with connection: 
            with connection.cursor() as cursor:
                cursor.execute(INSERT_NEW_ENTRY, (user_id, film_id,))
                
                new_watchlist_entry = cursor.fetchone()
                print(new_watchlist_entry, '<<<< NEW ENTRY')

                connection.commit()

                response_data = {
            "message": "New entry added", 
            "user_id": new_watchlist_entry[0],
            "film_id": new_watchlist_entry[1],
            "is_watched": new_watchlist_entry[2],
            "created_at": new_watchlist_entry[3]
            }

        return response_data
    
    except psycopg2.IntegrityError:
        abort(400, description='This fasdadfdasfailm has already been added.')
    # except psycopg2.IntegrityError:
    #     abort(409, description='This film has already been added.')
      