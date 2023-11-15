from dotenv import load_dotenv
import os
import requests
import json
from flask import Flask, jsonify

load_dotenv()

api_key = os.getenv("API_KEY")
api_token = os.getenv("API_TOKEN")


headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_token}"
}



def fetch_popular_films():

    base_url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    response = requests.get(base_url, headers=headers)
    
    print(api_token, "api_token")

    if response.status_code == 200:
        data = response.json()
        
        return jsonify(data['results'])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return {'error': response.status_code, 'msg': response.text}

def search_for_films(film):
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "query": film,
        "include_adult": False,
        "language": "en-US",
        "page": 1
        }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return(data['results'])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return {'error': {response.status_code}, 'msg': {response.text}}

def fetch_film_by_film_id(film_id):

    base_url = f"https://api.themoviedb.org/3/movie/{film_id}"
    params = {
        "language": "en-US",
        "append_to_response": "credits"
        }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return(data)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return {'error': {response.status_code}, 'msg': {response.text}}