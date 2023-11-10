import requests
from urllib.parse import urljoin
import pytest
from seed import seed_database

ENDPOINT="http://127.0.0.1:5000"


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
        "title", 
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

def test_get_film_by_title(seed_db):
    relative_url = '/films?title=Harry'
    url = ENDPOINT + relative_url
    response=requests.get(url)
    assert response.status_code == 200
    film_list = response.json()
    required_keys = [
        "id", 
        "title", 
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

def test_get_film_by_title_doesnt_exist(seed_db):
    relative_url = '/films?title=NoFilms'
    url = ENDPOINT + relative_url
    response=requests.get(url)
    assert response.status_code == 200
    film_not_found = response.json()
    assert film_not_found == {"message": "We couldn't find this film."}

#testing get films by film id endpoint
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

#testing invalid film id number
def test_get_films_by_film_id_invalid_id(seed_db):
    relative_url= ["/films/1"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 404
    response_text = response.json()
    assert response_text['message'] == "This film doesn't exist!"

#testing invalid input (not a number) for film id
def test_get_films_by_film_id_invalid_input(seed_db):
    relative_url= ["/films/cheese"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 400
    response_text = response.json()
    assert response_text['message'] == "Invalid ID!"
      
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
    
#testing invalid user id number
def test_get_users_by_user_id_invalid_id(seed_db):
    relative_url= ["/users/999"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 404
    response_text = response.json()
    assert response_text['message'] == "This user doesn't exist!"

#testing invalid input (not a number) for user id
def test_get_users_by_user_id_errors(seed_db):
    relative_url= ["/users/cheese"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 400
    response_text = response.json()
    assert response_text['message'] == "Invalid ID!"

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

#testing invalid user id number (get reviews)
def test_get_reviews_by_user_id_invalid_id(seed_db):
    relative_url= ["/users/999/reviews"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 404
    response_text = response.json()
    assert response_text['message'] == "This user doesn't exist!"

#testing invalid input (not a number) for user id (get reviews)
def test_get_reviews_by_user_id_errors(seed_db):
    relative_url= ["/users/cheese/reviews"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 400
    response_text = response.json()
    assert response_text['message'] == "Invalid ID!"

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

#testing invalid user id number (get watchlist)
def test_get_watchlist_by_user_id_invalid_id(seed_db):
    relative_url= ["/users/999/watchlist"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 404
    response_text = response.json()
    assert response_text['message'] == "This user doesn't exist!"

#testing invalid input (not a number) for user id (get watchlist)
def test_get_watchlist_by_user_id_errors(seed_db):
    relative_url= ["/users/cheese/watchlist"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 400
    response_text = response.json()
    assert response_text['message'] == "Invalid ID!"

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

#Generic 404 error handler
def test_invalid_path(seed_db):
    relative_url = ['/cheese']
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 404
    response_text = response.json()
    assert response_text["message"]=="cheese is not a valid path!"
 
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

    # testing get user by valid username endpoint
def test_get_user_by_username_endpoint(seed_db):
        username = "billy"
        relative_url = f'/users?username={username}'
        url = ENDPOINT + relative_url
        response=requests.get(url)
        assert response.status_code == 200
        user_data = response.json()
        print(user_data['user'], "LOG OF THING")
        assert user_data['user'][1] == username
        assert user_data['user'] == [
                                        2,
                                        "billy",
                                        "GOAT",
                                        "billy@yahrmyarmy.com"
                                    ]
    #testing get user by invalid username endpoint
def test_get_incorrect_user_by_username_endpoint(seed_db):
        username = "billyyy"
        relative_url = '/users?username=billyyy'
        url = ENDPOINT + relative_url
        response=requests.get(url)
        assert response.status_code == 404
        response_text = response.json()
        assert response_text['message'] == 'User not found'

    #testing get user without providing username query
def test_get_no_user_by_username_endpoint(seed_db):
        relative_url = '/users'
        url = ENDPOINT + relative_url
        response=requests.get(url)
        assert response.status_code == 400
        response_text = response.json()
        assert response_text['message'] == 'User query required'

def test_fetch_friends_by_user_id(seed_db):
        relative_url = '/users/2/friends'
        url = ENDPOINT + relative_url
        response=requests.get(url)
        assert response.status_code == 200
        required_keys = ["my_id", "friend_id", "friend_name", "friends_since"]
        if all(key in response for key in required_keys):
            assert True

def test_fetch_friends_by_user_id_no_friends(seed_db):
        relative_url = '/users/6/friends'
        url = ENDPOINT + relative_url
        response=requests.get(url)
        assert response.status_code == 200
        assert response.json() == {"message": "You have no friends!"}

#200 is a normal status code for a successful delete request 
#(or any request really)
#if we are returning a message back to the user

def test_delete_friends_by_friend_id(seed_db):
        relative_url = '/users/2/friends/1'
        url = ENDPOINT + relative_url
        response = requests.delete(url)
        assert response.status_code == 200
        assert response.json() == {'message': 'Friendship deleted successfully'}

def test_delete_friends_by_friend_id_no_friends(seed_db):
        relative_url = '/users/6/friends/1'
        url = ENDPOINT + relative_url
        response = requests.delete(url)
        assert response.status_code == 200
        assert response.json() == {'message': 'Friendship not found'}

        
