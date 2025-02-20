from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    role: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class Item(BaseModel):
    item_name : str
    item_description: str
    item_price: float


class Item(BaseModel):
    item_name : str
    item_description: str
    item_price: float