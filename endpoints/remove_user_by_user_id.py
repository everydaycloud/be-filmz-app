from flask import jsonify

def remove_user_by_user_id(user_id, connection):
    DELETE_USER_BY_USER_ID = """
    DELETE FROM users WHERE user_id = %s
    RETURNING *;
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_USER_BY_USER_ID, (user_id,))
            deleted_user = cursor.fetchone()

            if deleted_user:
                return jsonify({'message': f'User {deleted_user} deleted successfully'})
            else:
                return jsonify({'message': 'User not found'})
            