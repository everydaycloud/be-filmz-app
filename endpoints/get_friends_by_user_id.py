from flask import jsonify
                
def fetch_friends_by_user_id(user_id, connection):

    if user_id.isdigit():
        new_user_id = str(user_id)

        user_exists_query= "SELECT * FROM users WHERE user_id = %s;"
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(user_exists_query, (new_user_id,))
                user_exists = cursor.fetchone()

                if not user_exists:
                    return {"message": "This user doesn't exist!"}, 404

        friends_query = """
        SELECT u.username AS username, f.user_id AS user_id, uf.username AS friend_name, f.created_at AS friends_since, f.friend_id AS friend_id
        FROM friendships f
        JOIN users u ON f.user_id = u.user_id
        JOIN users uf ON f.friend_id = uf.user_id
        WHERE u.user_id = %s;
        """

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(friends_query, (new_user_id,))
                friends = cursor.fetchall()
                if friends:
                    result = []
                    for friend in friends:
                        result.append({
                            "my_id": friend[1], 
                            "friend_id": friend[4], 
                            "friend_name": friend[2], 
                            "friends_since": friend[3],
                        })  
                    return jsonify(result)
                else:
                    return {"message": "You have no friends!"}
    else:
        return {"message": "Invalid ID!"},400



                