import requests
from requests.auth import HTTPBasicAuth

url = "https://python-flask-apis.onrender.com/"

def test_secure_data_view():
    response = requests.get(url+"secure-data-view", auth=HTTPBasicAuth("testuser","secret"))
    print(response.status_code,response.text)
    assert response.status_code==200

def test_secure_data_admin():
    response = requests.get(url+"secure-data-admin", auth=HTTPBasicAuth("testuser","secret"))
    print(response.status_code,response.text)
    assert response.status_code==200
    response = requests.get(url+"secure-data-admin", auth=HTTPBasicAuth("testuser2","secret"))
    print(response.status_code,response.text)
    assert response.status_code==403

def test_token_login(username="testuser"):
    payload = 'username=%s&password=secret'%(username)
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url+"login", headers=headers, data=payload)
    print(response.status_code,response.text)
    assert response.status_code==200
    response_dict = response.json()
    access_token = response_dict["access_token"]
    return access_token
    

def test_secure_data_jwt_view(access_token):
    payload={}
    headers = {
    'Authorization': 'Bearer %s'%(access_token)
    }
    response = requests.request("GET", url+"secure-data-jwt-view", headers=headers, data=payload)
    print(response.status_code,response.text)
    assert response.status_code==200
    

def test_secure_data_jwt_admin(access_token):
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
    for i in range(1):
        response = requests.get(url+"secure-data-view", auth=HTTPBasicAuth("testuser","secret"))
        print(response.status_code,response.text)
        assert response.status_code==200
    response = requests.get(url+"secure-data-view", auth=HTTPBasicAuth("testuser","secret"))
    print(response.status_code,response.text)
    assert response.status_code==429


test_secure_data_view()
test_secure_data_admin()
access_token = test_token_login()
test_secure_data_jwt_view(access_token)
test_secure_data_jwt_admin(access_token)
test_rate_limit()