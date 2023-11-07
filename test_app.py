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
        


    
    

