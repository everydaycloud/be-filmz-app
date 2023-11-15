from flask import request, jsonify

GET_USERS = 'SELECT * FROM users;'

def authenticate_user(connection, data):

    user = data
    username = user.get('username')
    password = user.get('password')

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_USERS)
            users = cursor.fetchall() 

    user_data = {user[1]: {'password': user[2], 'avatar': user[4]} for user in users}
    
    if username not in user_data:
        return jsonify({"loggedIn": False, "message": "User not found"}), 401

    stored_password = user_data[username]['password']
    if password == stored_password:
        return jsonify({"loggedIn": True, "username": username, "avatar": user_data[username]['avatar']}), 200
    else:
        return jsonify({"loggedIn": False, "message": "Invalid password"}), 401
