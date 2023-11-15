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
			"username": "yahya",
            "avatar": "https://images.pexels.com/photos/16577552/pexels-photo-16577552/free-photo-of-a-kitten-with-a-toy.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
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

# testing get reviews by specific user ID endpoint
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

# testing adding new user
def test_add_new_user_endpoint(seed_db):
    relative_url = '/users'
    url = ENDPOINT + relative_url
    user_data = {
	    "username": "bigfilmfreakz",
	    "password": "filmzzz",
	    "email": "filmzz@yahmyarmy.com",
        "avatar": "https://images.pexels.com/photos/8172784/pexels-photo-8172784.jpeg?auto=compress&cs=tinysrgb&w=800"
    }

    response = requests.post(url, json=user_data)
    assert response.status_code == 200

    user = response.json()
    required_keys = ["id", "username", "email", "password", "avatar"]
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
    # response_text = response.json()
    # assert response_text["message"]=="cheese is not a valid path!"
 
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

#testing invalid id number (get reviews by film id)
def test_get_reviews_by_film_id_invalid_id(seed_db):
    relative_url= ["/films/1/reviews"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 404
    response_text = response.json()
    assert response_text['message'] == "This film doesn't exist!"

#testing invalid input (not a number)(get reviews by film id)
def test_get_reviews_by_film_id_errors(seed_db):
    relative_url= ["/films/cheese/reviews"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 400
    response_text = response.json()
    assert response_text['message'] == "Invalid ID!"

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
                                        "billy@yahrmyarmy.com",
                                        "https://images.pexels.com/photos/14603745/pexels-photo-14603745.jpeg?auto=compress&cs=tinysrgb&w=800"
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

#testing get friends by user id
def test_fetch_friends_by_user_id(seed_db):
        relative_url = '/users/2/friends'
        url = ENDPOINT + relative_url
        response=requests.get(url)
        assert response.status_code == 200
        required_keys = ["my_id", "friend_id", "friend_name", "friends_since"]
        if all(key in response for key in required_keys):
            assert True

#testing get friends by user id (no friends)
def test_fetch_friends_by_user_id_no_friends(seed_db):
        relative_url = '/users/6/friends'
        url = ENDPOINT + relative_url
        response=requests.get(url)
        assert response.status_code == 200
        assert response.json() == {"message": "You have no friends!"}

#testing invalid user id number (get friends by user id)
def test_get_friends_by_user_id_invalid_id(seed_db):
    relative_url= ["/users/999999/friends"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 404
    response_text = response.json()
    assert response_text['message'] == "This user doesn't exist!"

#testing invalid input (not a number)(get friends by user id)
def test_get_friends_by_user_id_errors(seed_db):
    relative_url= ["/users/cheese/friends"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)

    response = requests.get(url)
    assert response.status_code == 400
    response_text = response.json()
    assert response_text['message'] == "Invalid ID!"

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

def test_delete_user_by_user_id(seed_db):
        relative_url = '/users/5'
        url = ENDPOINT + relative_url
        response = requests.delete(url)
        assert response.status_code == 200
        assert response.json() == {"message": "User (5, 'barbara', 'fish', 'barbara@yahrmyarmy.com', 'https://images.pexels.com/photos/16352402/pexels-photo-16352402/free-photo-of-a-kitten-lying-in-purple-sheets.jpeg?auto=compress&cs=tinysrgb&w=800') deleted successfully"}        

def test_delete_review_by_id(seed_db):
        relative_url = '/reviews/7'
        url = ENDPOINT + relative_url
        response = requests.delete(url)
        assert response.status_code == 200
        assert response.json() == {"message": "Review (7, 4, 12445, 'An epic conclusion to an amazing series!', 5, 11, datetime.date(2023, 11, 13)) deleted successfully"}
        
        #testing (POST) adding new entry to watchlist
    #happy path
def test_add_new_user_endpoint(seed_db):
    user_id = 5
    relative_url = f'/users/5/watchlist'
    url = ENDPOINT + relative_url
    film_data = {
                "film_id":672
                }

    response = requests.post(url, json=film_data)
    assert response.status_code == 200


    result = response.json()
    required_keys = ["message", "created_at", "film_id", "is_watched", "user_id"]
    assert all(key in result for key in required_keys)
    
    #if film id = none
def test_add_to_watchlist_with_no_film_id(seed_db):
     relative_url = f'/users/6/watchlist'
     url = ENDPOINT + relative_url
     postObject = {"film_id": None}
     response = requests.post(url, json=postObject)
     assert response.status_code == 200
     response_text = response.json()

     assert 'message' in response_text
     assert response_text['message'] == 'film_id is required'

     #if film has already been added
def test_add_duplicate_film_to_watchlist_endpoint(seed_db):
     relative_url = '/users/6/watchlist'
     url = ENDPOINT + relative_url
     postObject = {"film_id": 672}
     response = requests.post(url, json=postObject)
     response = requests.post(url, json=postObject)
     assert response.status_code == 409
