import requests
from urllib.parse import urljoin

ENDPOINT="http://127.0.0.1:5000"

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

# testing get user by specific ID endpoint
def test_get_user_by_id_endpoint():
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
def test_get_reviews_by_user_id_endpoint():
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

 #Error tests (Need to be looked at later)       
def test_invalid_path():
    relative_url = ['/cheese']
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 404
    assert response.reason == "NOT FOUND"
 
 

