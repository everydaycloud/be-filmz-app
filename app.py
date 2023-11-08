import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from endpoints.fetch_all_films import fetch_all_films
from endpoints.fetch_films_by_film_id import fetch_films_by_film_id
from endpoints.add_user import add_new_user
from endpoints.get_reviews_by_user_id import get_reviews_by_user_id
from endpoints.get_reviews_by_film_id import fetch_reviews_by_film_id
from endpoints.get_user_by_user_id import get_user_by_user_id
from endpoints.get_watchlist_by_user_id import get_watchlist_by_user_id
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

@app.route("/films/<film_id>", methods=["GET"])
def get_films_by_film_id(film_id):
    result = fetch_films_by_film_id(connection, film_id)
    return result

# GET a user by user_id
@app.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
       return get_user_by_user_id(user_id, connection)

# GET reviews by user_id
@app.route('/users/<int:user_id>/reviews', methods=['GET'])
def get_reviews(user_id):
    return get_reviews_by_user_id(user_id, connection)

# GET reviews by (film)id
@app.route('/films/<int:film_id>/reviews', methods=['GET'])
def get_reviews_by_film_id(film_id):
    return fetch_reviews_by_film_id(film_id, connection)

# GET watchlist by user_id
@app.route('/users/<int:user_id>/watchlist', methods=['GET'])
def get_watchlist(user_id):
    return get_watchlist_by_user_id(user_id, connection)

@app.route("/users", methods=["POST"])
def post_new_user():
    data = request.get_json()
    result = add_new_user(data, connection)
    return jsonify(result)


# @app.route("/*")

# Error endpoint attempt (Not necessary for the current test to pass)
# @app.route('/<path:other>')
# def other_path(other):
#     return f'Error 404: "{other}" is an invalid path'