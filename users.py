from fastapi import Depends, FastAPI, HTTPException, status
from authentication import *
import json, os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pathlib import Path


#dummy database
with open(os.path.dirname(__file__)+"/data/users.json", 'r') as file:
    data = file.read()
db = json.loads(data)

app = FastAPI()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(                    
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]

@app.post("/createuser/")
async def create_new_user(User: User):
    if User.username is None or User.full_name is None or User.password is None or User.email is None or User.role is None:
        raise HTTPException(status_code=400, detail="Bad Request")
    else:
        db[User.full_name]={
        "username": User.username,
        "full_name": User.full_name,
        "email": User.email,
        "role": User.role,
        "hashed_password": get_password_hash(User.password),
        "disabled": False
    }
        with open(os.path.dirname(__file__)+"/data/users.json", 'w') as fp:
             json.dump(db, fp)
    return "User created sucessfully with the username %s"%(User.username)

