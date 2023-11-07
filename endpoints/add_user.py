INSERT_USER_RETURN_ID = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s) RETURNING id;"

def add_new_user(request, connection): 
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        email = data["email"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_USER_RETURN_ID, (name,))
                new_user = cursor.fetchall()
            return {"message": "New user created.", "id": new_user[0], "username": new_user[0], 
                    "password": new_user[1], "email": new_user[2]}