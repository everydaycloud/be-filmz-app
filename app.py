import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask

import json

load_dotenv()

app = Flask(__name__)

url = os.environ.get("dbname=filmz_app_test") # Might tweak later to test/local database
connection = psycopg2.connect(url)

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
            title=cursor.fetchone()[0]
    return {"title": title}          