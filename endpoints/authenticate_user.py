from flask import request, jsonify

GET_USERS = 'SELECT * FROM users;'

def authenticate_user(connection, data):
    print(data)

    user = data
    username = user.get('username')
    password = user.get('password')

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_USERS)
            users = cursor.fetchall() 

    user_usernames = [user[1] for user in users]
    if username not in user_usernames:
        return jsonify({"authenticated": False, "message": "User not found"}), 401

    user_passwords = {user[1]: user[2] for user in users}
    stored_password = user_passwords.get(username)
    if stored_password and password == stored_password:
        return jsonify({"authenticated": True, "message": "Authentication successful"}), 200
    else:
        return jsonify({"authenticated": False, "message": "Invalid password"}), 401
