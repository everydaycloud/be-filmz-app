from db.connection import get_connection
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from endpoints.fetch_all_films import fetch_all_films
from endpoints.fetch_films_by_film_id import fetch_films_by_film_id
from endpoints.add_user import add_new_user
from endpoints.get_reviews_by_user_id import get_reviews_by_user_id
from endpoints.get_reviews_by_film_id import fetch_reviews_by_film_id
from endpoints.get_user_by_user_id import get_user_by_user_id
from endpoints.get_watchlist_by_user_id import get_watchlist_by_user_id
from endpoints.add_new_friend import add_new_friend
from endpoints.fetch_user_by_username import fetch_user_by_username
from endpoints.get_tmbd_data import get_popular_films
from endpoints.get_tmbd_data import search_for_films
from endpoints.get_tmbd_data import get_film_by_film_id
from endpoints.get_friends_by_user_id import fetch_friends_by_user_id

import json

load_dotenv()

app = Flask(__name__)

# url = os.environ.get("dbname=filmz_app_test") # Might tweak later to test/local database
connection = get_connection()

# GET all endpoints
@app.route("/", methods=["GET"])
def get_endpoints():
    file = open("./endpoints.json")
    data = json.load(file)
    return data

# GET all films
@app.route("/films", methods=["GET"])
def get_all_films():
    result = fetch_all_films(connection)
    return result

# GET a film by film_id
@app.route("/films/<film_id>", methods=["GET"])
def get_films_by_film_id(film_id):
    result = fetch_films_by_film_id(connection, film_id)
    return result

# GET a user by user_id
@app.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
       return get_user_by_user_id(user_id, connection)

# GET reviews by user_id
@app.route('/users/<user_id>/reviews', methods=['GET'])
def get_reviews(user_id):
    return get_reviews_by_user_id(user_id, connection)

# GET reviews by (film)id
@app.route('/films/<film_id>/reviews', methods=['GET'])
def get_reviews_by_film_id(film_id):
    return fetch_reviews_by_film_id(film_id, connection)

# GET watchlist by user_id
@app.route('/users/<user_id>/watchlist', methods=['GET'])
def get_watchlist(user_id):
    return get_watchlist_by_user_id(user_id, connection)

# POST user
@app.route("/users", methods=["POST"])
def post_new_user():
    data = request.get_json()
    result = add_new_user(data, connection)
    return jsonify(result)

# GET username by username (query)
@app.route("/users", methods=["GET"])
def get_user_by_username():
    return fetch_user_by_username(connection)

# POST new friend to friends table 
@app.route("/users/<user_id>/friends", methods=["POST"])
def add_friend(user_id):
    data = request.get_json()
    result = (add_new_friend(data, connection, user_id))
    return jsonify(result)

@app.route("/tmdb/films/popular", methods=["GET"])
def get_tmdb_popular():
    return get_popular_films()

@app.route("/tmdb/films/<film>", methods=["GET"])
def get_tmdb_search(film):
    return search_for_films(film)

@app.route("/tmdb/films/<int:film_id>", methods=["GET"])
def get_tmdb_film(film_id):
    return get_film_by_film_id(film_id)

@app.route("/users/<user_id>/friends", methods=["GET"])
def get_friends_by_user_id(user_id):
    return fetch_friends_by_user_id(user_id, connection)
   
# @app.route("/*")

# Error endpoint attempt (Not necessary for the current test to pass)
# @app.route('/<path:other>')
# def other_path(other):
#     return f'Error 404: "{other}" is an invalid path'