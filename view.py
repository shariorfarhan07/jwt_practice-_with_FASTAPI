from pydantic import BaseModel

class AuthDetails(BaseModel):
    username: str
    password: str

class tweet(BaseModel):
    id : int
    user : str
    text : str


class user(BaseModel):
    id :int
    name : str
    password : str
