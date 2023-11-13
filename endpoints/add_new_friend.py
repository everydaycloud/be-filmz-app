INSERT_NEW_FRIEND = "INSERT INTO friendships (user_id, friend_id) VALUES (%s, %s) RETURNING user_id, friend_id;"

def add_new_friend(data, connection, user_id):
    friend_id = data["friend_id"]
    with connection: 
        with connection.cursor() as cursor:
              cursor.execute(INSERT_NEW_FRIEND, (user_id, friend_id,))
              cursor.execute(INSERT_NEW_FRIEND, (friend_id, user_id,))
              new_friendship = cursor.fetchone()

    return {
         "message": "New friendship added", 
         "user1": new_friendship[0],
         "user2": new_friendship[1]
         }
