import requests
from urllib.parse import urljoin
import pytest
from db.seeds.seed import seed_database


ENDPOINT="http://127.0.0.1:5000"

@pytest.fixture
def seed_db():
    seed_database()
    yield


def test_home_endpoint():
    relative_url = ["/"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)
    
    response=requests.get(url)
    assert response.status_code == 200

def test_get_all_films_endpoint():
    relative_url = ["/films"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 200
    film_list = response.json()
    required_keys = ["id", "original_title", "overview", "poster_path", 
               "release_date", "vote_average", "vote_count"]
    for film in film_list['films']:
        if all(key in film for key in required_keys):
            assert True
        else: assert False

def test_get_films_by_film_id():
    relative_url= ["/films/767"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    film = response.json()
    required_keys = ["id", "original_title", "overview", "poster_path", 
               "release_date", "vote_average", "vote_count"]
    if all(key in film for key in required_keys):
            assert True
    else: assert False
        
# testing get user by specific ID endpoint
def test_get_user_by_id_endpoint():
    relative_url = '/users/1'
    url = ENDPOINT + relative_url
    response=requests.get(url)
    assert response.status_code == 200    
    user = response.json()['user']
    assert len(user) == 4
    assert user[0] == 1
    assert user[1] == 'yahya'
    assert user[2] == 'pyramids'
    assert user[3] == 'yahya@yahrmyarmy.com'


def test_add_new_user_endpoint():
    relative_url = '/users'
    url = ENDPOINT + relative_url
    user_data = {
	    "username": "bigfilmfreakz",
	    "password": "filmzzz",
	    "email": "filmzz@yahmyarmy.com"
    }

    response = requests.post(url, json=user_data)
    assert response.status_code == 200

    user = response.json()
    required_keys = ["id", "username", "email", "password"]
    assert all(key in user for key in required_keys)

 #Error tests (Need to be looked at later)       

def test_invalid_path():
    relative_url = ['/cheese']
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 404
    assert response.reason == "NOT FOUND"
 
 

