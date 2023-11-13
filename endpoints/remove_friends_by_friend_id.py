from flask import jsonify

def remove_friends_by_friend_id(user_id, friend_id, connection):
    DELETE_FRIEND_BY_FRIEND_ID = """
    DELETE FROM friendships WHERE user_id = %s AND friend_id = %s
    RETURNING *;
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_FRIEND_BY_FRIEND_ID, (user_id, friend_id,))
            deleted_friend = cursor.fetchone()

            if deleted_friend:
                return jsonify({'message': 'Friendship deleted successfully'})
            else:
                return jsonify({'message': 'Friendship not found'})
            