import psycopg2
from dotenv import load_dotenv
from flask import Flask
from endpoints.fetch_all_films import fetch_all_films
from endpoints.fetch_films_by_film_id import fetch_films_by_film_id

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


# Error endpoint attempt (Not necessary for the current test to pass)
# @app.route('/<path:other>')
# def other_path(other):
#     return f'Error 404: "{other}" is an invalid path'