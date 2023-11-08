import psycopg2
from dotenv import load_dotenv
from flask import Flask
from endpoints.fetch_all_films import fetch_all_films
from endpoints.add_user import add_new_user
from endpoints.get_reviews_by_film_id import fetch_reviews_by_film_id

from flask import jsonify

import json

load_dotenv()

app = Flask(__name__)

# url = os.environ.get("dbname=filmz_app_test") # Might tweak later to test/local database
connection = psycopg2.connect("dbname=filmz_app_test")

@app.route("/", methods=["GET"])
def get_endpoints():
    file = open("./endpoints.json")
    data = json.load(file)
    return data

@app.route("/films", methods=["GET"])
def get_all_films():
    result = fetch_all_films(connection)
    return result

# GET a user by user_id
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE user_id = (%s);', (user_id,))
            user = cursor.fetchone()
    return {'user': user}

# GET reviews by (film)id
@app.route('/films/<int:film_id>/reviews', methods=['GET'])
def get_reviews_by_film_id(film_id):
    return fetch_reviews_by_film_id(film_id, connection)
        

@app.route("/users", methods=["POST"])
def post_new_user(request):
    result = add_new_user(request, connection)
    return result


# @app.route("/*")

# Error endpoint attempt (Not necessary for the current test to pass)
# @app.route('/<path:other>')
# def other_path(other):
#     return f'Error 404: "{other}" is an invalid path'