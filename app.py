import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify
# from db.seeds.seed import connection

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
    with connection: 
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM films;')
            films=cursor.fetchall()
            if films:
                result = []
                for film in films:
                    result.append({"id": film[3], "original_title": film[5], "overview": film[6], "poster_path": film[8],
                                   "release_date": film[9], "vote_average": film[12], "vote_count": film[13]})
    return {"films": result}

# @app.route("/*")