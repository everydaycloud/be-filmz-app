import requests
from urllib.parse import urljoin
import pytest
from db.seeds.seed import seed_database

ENDPOINT="http://127.0.0.1:5000"

# reseed after test 
@pytest.fixture(autouse=True)
def seed_db():
    seed_database()
    yield

def test_home_endpoint(seed_db):
    relative_url = ["/"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)
    
    response=requests.get(url)
    assert response.status_code == 200

def test_get_all_films_endpoint(seed_db):
    relative_url = ["/films"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 200
    film_list = response.json()
    required_keys = [
        "id", 
        "original_title", 
        "overview", 
        "poster_path", 
        "release_date", 
        "vote_average", 
        "vote_count"
        ]
    for film in film_list['films']:
        if all(key in film for key in required_keys):
            assert True
        else: assert False

def test_get_films_by_film_id(seed_db):
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
def test_get_user_by_id_endpoint(seed_db):
    relative_url = '/users/1'
    url = ENDPOINT + relative_url
    response=requests.get(url)
    assert response.status_code == 200    
    user = response.json()['user']
    assert len(user) == 1
    assert user[0] == {
			"email": "yahya@yahrmyarmy.com",
			"password": "pyramids",
			"user_id": 1,
			"username": "yahya"
		}

# testing get revies by specific user ID endpoint
def test_get_reviews_by_user_id_endpoint(seed_db):
    relative_url = '/users/2/reviews'
    url = ENDPOINT + relative_url
    response=requests.get(url)
    assert response.status_code == 200    
    returned_reviews = response.json()['reviews']
    assert isinstance(returned_reviews, list)
    assert len(returned_reviews) == 3
    expected_review_structure = {
        "body": str,
        "created_at": str,
        "email": str,
        "film_id": int,
        "password": str,
        "rating": int,
        "review_id": int,
        "user_id": int,
        "username": str,
        "votes": int
    }
    for review in returned_reviews:
        assert all(key in review for key in expected_review_structure)

# testing get reviews by specific user ID endpoint
def test_get_watchlist_by_user_id_endpoint(seed_db):
    relative_url = '/users/3/watchlist'
    url = ENDPOINT + relative_url
    response=requests.get(url)
    assert response.status_code == 200    
    returned_watchlist = response.json()['watchlist']
    assert isinstance(returned_watchlist, list)
    assert len(returned_watchlist) == 2
    expected_keys = {
        "backdrop_path", 
        "created_at", 
        "film_id", 
        "is_watched", 
        "title", 
        "vote_average"
    }
    for item in returned_watchlist:
        assert set(item.keys()) == expected_keys

def test_add_new_user_endpoint(seed_db):
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

# testing adding new friend
def test_add_new_friend_endpoint(seed_db):
    relative_url = '/users/1/friends'
    url = ENDPOINT + relative_url
    friend_data = {
	    "friend_id": 5
    }

    response = requests.post(url, json=friend_data)
    assert response.status_code == 200

    result = response.json()
    required_keys = ["message", "user1", "user2"]
    assert all(key in result for key in required_keys)

 #Error tests (Need to be looked at later)       

def test_invalid_path(seed_db):
    relative_url = ['/cheese']
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 404
    assert response.reason == "NOT FOUND"
 
 

