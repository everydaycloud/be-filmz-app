from db.connection import get_connection
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from endpoints.fetch_all_films import fetch_all_films
from endpoints.fetch_films_by_film_id import fetch_films_by_film_id
from endpoints.add_user import add_new_user
from endpoints.fetch_reviews_by_user_id import fetch_reviews_by_user_id
from endpoints.fetch_reviews_by_film_id import fetch_reviews_by_film_id
from endpoints.fetch_user_by_user_id import fetch_user_by_user_id
from endpoints.fetch_watchlist_by_user_id import fetch_watchlist_by_user_id
from endpoints.add_new_friend import add_new_friend
from endpoints.fetch_user_by_username import fetch_user_by_username
from endpoints.fetch_tmbd_data import fetch_popular_films
from endpoints.fetch_tmbd_data import search_for_films
from endpoints.fetch_tmbd_data import fetch_film_by_film_id
from endpoints.add_new_watchlist_entry import add_new_entry
from endpoints.fetch_friends_by_user_id import fetch_friends_by_user_id
from endpoints.remove_friends_by_friend_id import remove_friends_by_friend_id
from endpoints.remove_user_by_user_id import remove_user_by_user_id
from endpoints.remove_review_by_id import remove_review_by_id
from endpoints.add_review_by_film_id import add_review_by_film_id
from endpoints.patch_is_watched import toggle_is_watched
from endpoints.authenticate_user import authenticate_user
from endpoints.remove_watchlist_entry import remove_watchlist_entry


import json

load_dotenv()

app = Flask(__name__)
CORS(app)

connection = get_connection()

# GET all endpoints
@app.route("/", methods=["GET"])
@cross_origin() 
def get_endpoints():
    file = open("./endpoints.json")
    data = json.load(file)
    return data

# GET all films
@app.route("/films", methods=["GET"])
@cross_origin() 
def get_all_films():
    result = fetch_all_films(connection)
    return result

# GET a film by film_id
@app.route("/films/<film_id>", methods=["GET"])
@cross_origin() 
def get_films_by_film_id(film_id):
    result = fetch_films_by_film_id(connection, film_id)
    return result

# GET a user by user_id
@app.route('/users/<user_id>', methods=['GET'])
@cross_origin() 
def get_single_user(user_id):
       return fetch_user_by_user_id(user_id, connection)

# GET reviews by user_id
@app.route('/users/<user_id>/reviews', methods=['GET'])
@cross_origin() 
def get_reviews(user_id):
    return fetch_reviews_by_user_id(user_id, connection)

# GET reviews by film_id
@app.route('/films/<film_id>/reviews', methods=['GET'])
@cross_origin() 
def get_reviews_by_film_id(film_id):
    return fetch_reviews_by_film_id(film_id, connection)

# GET watchlist by user_id
@app.route('/users/<user_id>/watchlist', methods=['GET'])
@cross_origin() 
def get_watchlist(user_id):
    return fetch_watchlist_by_user_id(user_id, connection)

# POST user
@app.route("/users", methods=["POST"])
@cross_origin() 
def post_new_user():
    data = request.get_json()
    result = add_new_user(data, connection)
    return jsonify(result)

# GET username by username (query)
@app.route("/users", methods=["GET"])
@cross_origin() 
def get_user_by_username():
    return fetch_user_by_username(connection)

# POST new friend to friends table 
@app.route("/users/<user_id>/friends", methods=["POST"])
@cross_origin() 
def add_friend(user_id):
    data = request.get_json()
    result = (add_new_friend(data, connection, user_id))
    return jsonify(result)

# POST new entry to watchlist
@app.route("/users/<int:user_id>/watchlist", methods=["POST"])
def add_watchlist_entry(user_id):
    data = request.get_json()
    film_id = data["film_id"]
    result = (add_new_entry(film_id, connection, user_id))
    return jsonify(result)

@app.route("/tmdb/films/popular", methods=["GET"])
@cross_origin() 
def get_tmdb_popular():
    return fetch_popular_films()

@app.route("/tmdb/films/<film>", methods=["GET"])
@cross_origin() 
def get_tmdb_search(film):
    return search_for_films(film)

@app.route("/tmdb/films/<int:film_id>", methods=["GET"])
@cross_origin() 
def get_tmdb_film(film_id):
    return fetch_film_by_film_id(film_id)

# GET friends by user id
@app.route("/users/<user_id>/friends", methods=["GET"])
@cross_origin() 
def get_friends_by_user_id(user_id):
    return fetch_friends_by_user_id(user_id, connection)

@app.route("/users/<int:user_id>/friends/<friend_id>", methods=["DELETE"])
@cross_origin() 
def delete_friends_by_friend_id(user_id, friend_id):
    return remove_friends_by_friend_id(user_id, friend_id, connection)

# DELETE user by id 
@app.route("/users/<int:user_id>", methods=["DELETE"])
@cross_origin() 
def delete_user_by_user_id(user_id):
    return remove_user_by_user_id(user_id, connection)

# DELETE review by id
@app.route("/reviews/<int:review_id>", methods=["DELETE"])
@cross_origin() 
def delete_review_by_id(review_id):
    return remove_review_by_id(review_id, connection)

# POST Authentication for user
@app.route("/authenticate", methods=["POST"])
@cross_origin() 
def check_authentication():
    data = request.get_json()
    return authenticate_user(connection, data)

# PATCH isWatched by film_id

@app.route("/users/<user_id>/watchlist/<film_id>", methods=["PATCH"])
@cross_origin()
def patch_is_watched_property(user_id, film_id):
    #currently takes a request object in the form {"is_watched":"true/false"}, boolean has to be written as a string to be parsed correctly
    data = request.get_json()
    is_watched_update = data["is_watched"]
    return toggle_is_watched(user_id, film_id, connection, is_watched_update)

#Any other path
@app.route('/<path:other>')
@cross_origin()
def other_path(other):
    return {"message": f"{other} is not a valid path!"},404

#post review by film id
@app.route('/films/<film_id>/reviews', methods=["POST"])
@cross_origin()
def post_review_by_film_id(film_id):
    data = request.get_json()
    return add_review_by_film_id(data, film_id, connection)

#delete watchlist entry
@app.route("/users/<int:user_id>/watchlist", methods=["DELETE"])
def delete_watchlist(user_id):
    data = request.get_json()
    film_id = data["film_id"]
    return remove_watchlist_entry(user_id, film_id, connection)
