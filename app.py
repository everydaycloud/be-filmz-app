import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask

import json

load_dotenv()

app = Flask(__name__)

url = os.environ.get("DATABASE_URL") # Might tweak later to test/local database
connection = psycopg2.connect(url)

@app.route("/", methods=["GET"])
def get_endpoints():
    file = open("./endpoints.json")
    data = json.load(file)
    return data
