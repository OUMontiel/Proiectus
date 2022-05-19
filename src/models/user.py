from abc import ABC, abstractmethod
from beanie import Document, PydanticObjectId
from email_validator import validate_email, EmailNotValidError
from enum import Enum
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, Field
from pymongo.database import Database
from typing import Any, Optional

templates = Jinja2Templates(directory="templates")


class UserTypeEnum(str, Enum):
    student = 'student'
    professor = 'professor'


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    user_type: UserTypeEnum

class UserIn(UserBase):
    '''Campos del usuario que son recibidos en un nuevo registro'''
    password: str
class UserOut(UserBase):
    '''Campos del usuario que se regresan al cliente''' #TODO Standarize docs lang
    id: PydanticObjectId

class UserModel(Document, UserOut):
    
    password: str
    class Settings:
        name = 'user'

    @classmethod
    def from_mongo_doc(cls, doc: Any) -> 'UserModel':
        instance = UserModel(
            id=str(doc['_id']),
            first_name=doc['first_name'],
            last_name=doc['last_name'],
            email=doc['email'],
            user_type=doc['user_type'],
        )
        return instance
