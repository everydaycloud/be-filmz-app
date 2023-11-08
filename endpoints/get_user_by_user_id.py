from flask import jsonify

def get_user_by_user_id(user_id, connection):    
    with connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                               SELECT * 
                               FROM users 
                               WHERE user_id = (%s);
                               ''', (user_id,))
                result = cursor.fetchall()
                column_names = cursor.description
                column_names = [desc[0] for desc in cursor.description]

    user = [dict(zip(column_names, row)) for row in result]
    return jsonify({'user': user})  