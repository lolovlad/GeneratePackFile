from typing import List
from enum import Enum
from pydantic import BaseModel, UUID4, field_serializer


class TypeUser(BaseModel):
    id: int
    name: str
    description: str


class UserUUID(BaseModel):
    uuid: UUID4

    @field_serializer('uuid')
    def serialize_dt(self, dt: UUID4, _info):
        return str(dt)


class UserBase(BaseModel):
    email: str
    name: str
    surname: str
    patronymic: str
    phone: str


class UserGet(UserBase, UserUUID):
    type: TypeUser


class UserPost(UserBase):
    password: str
    id_type: int


class UserUpdate(UserBase):
    password: str
    id_type: int

