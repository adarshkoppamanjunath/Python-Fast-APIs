from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    role:  str or None = None
    disabled: bool or None = None
    password: str or None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str or None = None

class UserInDB(User):
    hashed_password: str