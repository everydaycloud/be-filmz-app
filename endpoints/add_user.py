CHECK_DUPLICATE_USER = 'SELECT * FROM users WHERE username = %s OR email = %s;'
INSERT_USER_RETURN_ID = "INSERT INTO users (username, password, email, avatar) VALUES (%s, %s, %s, %s) RETURNING user_id;"

def add_new_user(data, connection): 
    username = data["username"]
    password = data["password"]
    email = data["email"]
    avatar = data["avatar"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CHECK_DUPLICATE_USER, (username, email))
            existing_user = cursor.fetchone()

    if existing_user:
        return {
            "message": "Username or email already exists.",
            "id": existing_user[0],
            "username": existing_user[1],
            "email": existing_user[3],
        }, 409

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER_RETURN_ID, (username, password, email, avatar,))
            new_user = cursor.fetchone()

    return {
        "message": "New user created.", 
        "id": new_user[0], 
        "username": username, 
        "email": email,
        "avatar": avatar
    }, 200