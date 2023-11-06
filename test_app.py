import requests
from urllib.parse import urljoin

ENDPOINT="http://127.0.0.1:5000"

def test_home_endpoint():

    relative_url = ["/"]
    for rel_url in relative_url:
        url = urljoin(ENDPOINT, rel_url)
    
    response=requests.get(url)
    assert response.status_code == 200



