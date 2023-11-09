INSERT_USER_RETURN_ID = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s) RETURNING user_id;"

def add_new_user(data, connection): 
        username = data["username"]
        password = data["password"]
        email = data["email"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_USER_RETURN_ID, (username, password, email,))
                new_user = cursor.fetchone()
        return {
             "message": "New user created.", 
             "id": new_user[0], 
             "username": username, 
             "password": password, 
             "email": email
            }