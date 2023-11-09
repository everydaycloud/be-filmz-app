from flask import jsonify, request

def fetch_user_by_username(connection):
#   print("i'm in")
  username = request.args.get('username') #username referes to the query
#   print(username,"USERNAME")
  if username:
    with connection: 
      with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username =%s;",(username,))
        user=cursor.fetchone()
        
        if user:
            result = {
                'user_id': user[0],
                'username': user[1],
                'password': user[2],
                'email': user[3]
            }
            return jsonify(result)