import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)

url = os.environ.get("DATABASE_URL") # Might tweak later to test/local database
connection = psycopg2.connect(url)

@app.get("/")
def home():
    return "hello world"