# FastAPI with SQLite Deployment on Render

This is a simple ***FastAPI*** application with ***basic*** and ***JWT*** authentication and authorization that uses ***SQLite*** as its database backend. The app is designed to be easily deployed on ***Render*** and provides basic endpoints with ***a rate limit.*** Also includes ***basic CRUD*** endpoints.


## The app can be accessed at

```bash
https://python-flask-apis.onrender.com/docs
```

## To use this locally,

- Insatall Python 3
- Install required libraries `pip install -r requirements.txt`
- Start app `uvicorn app.main:app --reload`. Can be accessed at `http://127.0.0.1:8000/docs`
- Run tests `Python tests\unit_tests.py`
- You need these two users if you are using this to learn API test  
    - User1 with admin role 
        - username:   `testuser`
        - password:   `secret`
     - User2 with view role 
        - username:   `testuser2`
        - password:   `secret`

