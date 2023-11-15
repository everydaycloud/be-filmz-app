from flask import jsonify

def remove_watchlist_entry(user_id, film_id, connection):
    DELETE_WATCHLIST_ENTRY = """
    DELETE FROM watchlist WHERE user_id = %s AND film_id = %s
    RETURNING *;
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_WATCHLIST_ENTRY, (user_id, film_id,))
            deleted_entry = cursor.fetchone()

            if deleted_entry:
                return jsonify({'message': 'Watchlist entry deleted successfully'})
            else:
                return jsonify({'message': 'Watchlist entry not found'})