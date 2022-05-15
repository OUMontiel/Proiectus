from abc import ABC, abstractmethod
from email_validator import validate_email, EmailNotValidError
from enum import Enum
from pydantic import BaseModel
from pymongo.database import Database
from typing import Optional
from utils.auth import AuthHandler

class UserTypeEnum(str, Enum):
    student = 'student'
    professor = 'professor'

# ---------------------------------
# Pydantic Models (Types)
# ---------------------------------

class UserModel(BaseModel):
    id: Optional[str]
    first_name: str
    last_name: str
    email: str
    user_type: UserTypeEnum

class UserIn(UserModel):
    password: str

class UserOut(UserModel):
    pass

# ---------------------------------
# Factory method: Products
# ---------------------------------
class User(ABC):
    @abstractmethod
    def __init__(self, user_in: UserIn):
        pass

class Student(User):
    user_type = UserTypeEnum.student

    def __init__(self, user_in: UserIn):
        self.id = user_in.id
        self.first_name = user_in.first_name
        self.last_name = user_in.last_name
        self.email = user_in.email
        self.password = user_in.password

class Professor(User):
    user_type = UserTypeEnum.professor

    def __init__(self, user_in: UserIn):
        self.id = user_in.id
        self.first_name = user_in.first_name
        self.last_name = user_in.last_name
        self.email = user_in.email
        self.password = user_in.password

# ---------------------------------
# Factory method: Creators
# ---------------------------------
class UserCreatorBlueprint(ABC):

    @abstractmethod
    def createUser(self, user_in: UserIn):
        pass

    async def registerUser(self, db: Database, user: UserIn) -> dict:
        new_user = self.createUser(user)
        # Required fields
        if (not user.first_name or not user.last_name
            or not user.email or not user.password):
            raise HTTPException(status_code=400, detail="Missing fields.")

        # Validate email
        try:
            user.email = user.email.lower()
            user.email = validate_email(user.email).email
        except EmailNotValidError as e:
            raise HTTPException(status_code=400, detail="Email is not valid.")

        # Check for duplicates
        if db.user.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="This email already exists")

        auth_handler = AuthHandler()
        user.password = auth_handler.hash_password(user.password)
        del user.id
        
        id = db.user.insert_one(dict(user)).inserted_id
        token = auth_handler.encode_token(str(id))
        return { 'token': token }


class StudentCreator(UserCreatorBlueprint):
    
    def createUser(self, user_in: UserIn) -> User:
        return Student(user_in)

class ProfessorCreator(UserCreatorBlueprint):

    def createUser(self, user_in: UserIn) -> User:
        return Professor(user_in)