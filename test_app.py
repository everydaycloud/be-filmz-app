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
    required_keys = ["id", "original_title", "overview", "poster_path", 
               "release_date", "vote_average", "vote_count"]
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
    assert len(user) == 4
    assert user[0] == 1
    assert user[1] == 'yahya'
    assert user[2] == 'pyramids'
    assert user[3] == 'yahya@yahrmyarmy.com'

 #Error tests (Need to be looked at later)       

def test_invalid_path():
    relative_url = ['/cheese']
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 404
    assert response.reason == "NOT FOUND"
 
 
# testing get reviews by specific ID endpoint
def test_get_reviews_by_film_id_endpoint():
    relative_url = '/films/671/reviews'
    url = ENDPOINT + relative_url
    response=requests.get(url)
    assert response.status_code == 200    
    reviews = response.json()['reviews']
    assert len(reviews) == 2
    assert reviews[0] == {
      "body": "This movie is pure magic!",
      "created_at": "Tue, 07 Nov 2023 00:00:00 GMT",
      "film_id": 671,
      "rating": 5,
      "review_id": 1,
      "user_id": 1,
      "votes": 10
    }
    assert reviews[1] == {
      "body": "The magic of the first movie is unforgettable!",
      "created_at": "Sun, 12 Nov 2023 00:00:00 GMT",
      "film_id": 671,
      "rating": 5,
      "review_id": 6,
      "user_id": 5,
      "votes": 12
    }