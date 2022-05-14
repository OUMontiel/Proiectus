from typing import Optional
from enum import Enum

from pydantic import BaseModel

class UserTypeEnum(str, Enum):
    student = 'student'
    professor = 'professor'

class AuthDetails(BaseModel):
    email: str
    password: str

class User(AuthDetails):
    id: Optional[str]
    first_name: str
    last_name: str
    user_type: UserTypeEnum
