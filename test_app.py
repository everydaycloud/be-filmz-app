import requests

ENDPOINT="http://127.0.0.1:5000"

def test_home_endpoint():
    response=requests.get(ENDPOINT)
    assert response.status_code == 200

