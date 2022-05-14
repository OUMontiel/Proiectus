from typing import Optional
from enum import Enum

from pydantic import BaseModel

class UserTypeEnum(str, Enum):
    student = 'student'
    professor = 'professor'

class User(BaseModel):
    id: Optional[str]
    first_name: str
    last_name: str
    email: str
    password: str
    user_type: UserTypeEnum
