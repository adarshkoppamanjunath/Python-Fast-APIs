import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://python-flask-apis.onrender.com/"

def test_secure_data_view():
    print("\nTest no: 1, to test secure-data-view endpoint\n")
    response = requests.get(url+"secure-data-view", auth=HTTPBasicAuth("testuser","secret"))
    print(response.status_code,response.text)
    assert response.status_code==200

def test_secure_data_admin():
    print("\nTest no: 2, to test secure-data-admin endpoint\n")
    response = requests.get(url+"secure-data-admin", auth=HTTPBasicAuth("testuser","secret"))
    print(response.status_code,response.text)
    assert response.status_code==200
    response = requests.get(url+"secure-data-admin", auth=HTTPBasicAuth("testuser2","secret"))
    print(response.status_code,response.text)
    assert response.status_code==403

def test_token_login(username="testuser"):
    print("\nTest no: 3, to test login endpoint\n")
    payload = 'username=%s&password=secret'%(username)
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url+"login", headers=headers, data=payload)
    print(response.status_code,response.text)
    assert response.status_code==201
    response_dict = response.json()
    access_token = response_dict["access_token"]
    return access_token
    
def test_secure_data_jwt_view(access_token):
    print("\nTest no: 4, to test secure-data-jwt-view endpoint\n")
    payload={}
    headers = {
    'Authorization': 'Bearer %s'%(access_token)
    }
    response = requests.request("GET", url+"secure-data-jwt-view", headers=headers, data=payload)
    print(response.status_code,response.text)
    assert response.status_code==200
    
def test_secure_data_jwt_admin(access_token):
    print("\nTest no: 5, to test secure-data-jwt-admin endpoint\n")
    payload={}
    headers = {
    'Authorization': 'Bearer %s'%(access_token)
    }
    response = requests.request("GET", url+"secure-data-jwt-admin", headers=headers, data=payload)
    print(response.status_code,response.text)
    assert response.status_code==200
    access_token = test_token_login("testuser2")
    headers = {
    'Authorization': 'Bearer %s'%(access_token)
    }
    response = requests.request("GET", url+"secure-data-jwt-admin", headers=headers, data=payload)
    print(response.status_code,response.text)
    assert response.status_code==403

def test_rate_limit():
    print("\nTest no: 6, to test rate limit i.e 5 per minute on secure-data-view endpoint\n")
    for i in range(4):
        response = requests.get(url+"secure-data-view", auth=HTTPBasicAuth("testuser","secret"))
        print(response.status_code,response.text)
        assert response.status_code==200
    response = requests.get(url+"secure-data-view", auth=HTTPBasicAuth("testuser","secret"))
    print(response.status_code,response.text)
    assert response.status_code==429

def test_add_new_item(access_token):
    print("\nTest no: 7, to test add-new-item endpoint\n")
    payload = json.dumps({
    "item_name": "Samsung Galaxy",
    "item_description": "8GB RAM, 8MP Front Camera",
    "item_price": 750
    })
    headers = {
    'Authorization': 'Bearer %s'%(access_token),
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url+"add-new-item", headers=headers, data=payload)
    print(response.status_code,response.text)
    assert response.status_code==201
    return 750


test_secure_data_view()
test_secure_data_admin()
access_token = test_token_login()
test_secure_data_jwt_view(access_token)
test_secure_data_jwt_admin(access_token)
test_rate_limit()
item_id = test_add_new_item(access_token)