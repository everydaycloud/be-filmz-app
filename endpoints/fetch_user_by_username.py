from flask import jsonify, request

def fetch_user_by_username(connection):
#   print("i'm in")
  username = request.args.get('username') #username refers to the query
#   print(username,"USERNAME")
  if username:
    with connection: 
      with connection.cursor() as cursor:
        cursor.execute("""
                       SELECT * 
                       FROM users 
                       WHERE username = %s;
                       """,(username,))
        user=cursor.fetchone()
        
        if user:
            return jsonify({'user': user}), 200
        else: return {'message': 'User not found'}, 404
  else: return {'message': 'User query required'}, 400