import bcrypt, jwt
import json
import openai
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBasic
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.main import logger
from app.models.basemodel import *
from app.db.database import *

# basic auth
security = HTTPBasic()

# for jwt
SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# create access token with the time limit
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# before issuing token, we need to validate username and password
def authenticate_user(username: str, password: str):
    if username!="testuser" and username!="testuser2":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    username = authenticate_user_for_token(username,password)
    return username

# to validate token for jwt.
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
#to validate basic auth password.
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

#to validate jwt auth password.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#to validate password before issuing token for jwt.
def authenticate_user_for_token(username,password):
    con = get_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    con.close()
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": username}

# to validate credentials for basic auth.
def authenticate_user_detail(credentials: HTTPBasicCredentials = Depends(security)):
    con = get_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (credentials.username,))
    user = cursor.fetchone()
    con.close()
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": credentials.username}

#to validate required role for the particular user- authorization (basicAuth).
def require_role_ba(role: str):
    def role_checker(credentials: HTTPBasicCredentials = Depends(security)):
        return check_role(role,credentials.username)
    return role_checker

#to validate required role for the particular user- authorization (JWT).
def require_role_jwt(role: str):
    def role_checker(token: str = Depends(oauth2_scheme)):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        return check_role(role, username)
    return role_checker

#to validate role.
def check_role(role,user):
    con = get_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (user,))
    user_detail = cursor.fetchone()
    con.close()
    if user_detail["role"] != role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return user_detail["role"]

def convert_sql_result_to_json(db_name):
    icon = get_inventory_db()
    cursor = icon.cursor()
    cursor.execute("Select * from %s"%(db_name))
    all_items = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    result = {"all_items":[]}
    icon.close()
    for row in all_items:
        result["all_items"].append(dict(zip(columns, row)))
    return result

def log_to_container(message:str):
    print(f"{message}")

async def get_ai_response(message: str) -> str:
    response = openai.Completion.create(
        model="text-davinci-003",  # Change based on the model you're using
        prompt=message,
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].text.strip()
