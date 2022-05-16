from abc import ABC, abstractmethod
from email_validator import validate_email, EmailNotValidError
from enum import Enum
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pymongo.database import Database
from typing import Any, Optional
from utils.auth import AuthHandler

templates = Jinja2Templates(directory="templates")


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

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

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


class UserIn(UserModel):
    password: str

class UserOut(UserModel):
    pass

# ---------------------------------
# Factory method: Products
# ---------------------------------
class User(ABC):

    _state = None

    @abstractmethod
    def __init__(self):
        self.transition_to(LoggedOutState) # Default state

    def transition_to(self, state):
        self._state = state
        self._state._user = self

    def goToHome(self, request):
        return self._state.goToHome(self._state, request)

    def goToRegister(self, request):
        return self._state.goToRegister(self._state, request)

    def goToDashboard(self, request, context={}):
        return self._state.goToDashboard(self._state, request, context)

    def goToNewProject(self, request):
        return self._state.goToNewProject(self._state, request)

class Student(User):
    user_type = UserTypeEnum.student

    def __init__(self, user_in: UserIn):
        super().__init__()
        self.id = user_in["id"]
        self.first_name = user_in["first_name"]
        self.last_name = user_in["last_name"]
        self.email = user_in["email"]
        self.password = user_in["password"]

class Professor(User):
    user_type = UserTypeEnum.professor

    def __init__(self, user_in: UserIn):
        super().__init__()
        self.id = user_in["id"]
        self.first_name = user_in["first_name"]
        self.last_name = user_in["last_name"]
        self.email = user_in["email"]
        self.password = user_in["password"]

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
        if (not user["first_name"] or not user["last_name"]
            or not user["email"] or not user["password"]):
            raise HTTPException(status_code=400, detail="Missing fields.")

        # Validate email
        try:
            user["email"] = user["email"].lower()
            user["email"] = validate_email(user["email"]).email
        except EmailNotValidError as e:
            raise HTTPException(status_code=400, detail="Email is not valid.")

        # Check for duplicates
        if db.user.find_one({"email": user["email"]}):
            raise HTTPException(status_code=400, detail="This email already exists")

        auth_handler = AuthHandler()
        user["password"] = auth_handler.hash_password(user["password"])
        del user["id"]
        
        id = db.user.insert_one(user).inserted_id
        token = auth_handler.encode_token(str(id))
        return { 'token': token }


class StudentCreator(UserCreatorBlueprint):
    
    def createUser(self, user_in: UserIn) -> User:
        return Student(user_in)

class ProfessorCreator(UserCreatorBlueprint):

    def createUser(self, user_in: UserIn) -> User:
        return Professor(user_in)

# ---------------------------------
# State: States
# ---------------------------------
class UserState(ABC):

    _user = None

    @abstractmethod
    def goToHome(self, request):
        pass

    @abstractmethod
    def goToRegister(self, request):
        pass

    @abstractmethod
    def goToDashboard(self, request, context={}):
        return self.goToDefault(request)

    @abstractmethod
    def goToNewProject(self, request):
        pass

class LoggedInState(UserState):
    
    def goToHome(self, request):
        return RedirectResponse("/dashboard")

    def goToRegister(self, request):
        return RedirectResponse("/dashboard")

    def goToDashboard(self, request, context={}):
        return templates.TemplateResponse("dashboard.html", {"request": request, "user": self._user, **context})

    def goToNewProject(self, request):
        pass

class LoggedOutState(UserState):
    
    def goToHome(self, request):
        return templates.TemplateResponse("index.html", { "request": request })

    def goToRegister(self, request):
        return templates.TemplateResponse("registration.html", { "request": request })

    def goToDashboard(self, request, context={}):
        return RedirectResponse("/")

    def goToNewProject(self, request):
        pass