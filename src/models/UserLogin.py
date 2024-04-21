from pydantic import BaseModel
from .User import UserGet


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: UserGet


class UserSigIn(BaseModel):
    user: UserGet
    token: Token


class UserLogin(BaseModel):
    login: str
    password: str


class UserSignup(BaseModel):
    email: str
    name: str
    surname: str
    patronymic: str
    phone: str
    password: str
