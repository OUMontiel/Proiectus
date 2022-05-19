from abc import ABC, abstractmethod
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from pymongo.database import Database
from models.user import UserIn, UserModel, UserTypeEnum
from utils.auth import AuthHandler

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

# ---------------------------------
# Factory method: Products
# ---------------------------------


class User(ABC):

    _state = None

    @abstractmethod
    def __init__(self):
        self.transition_to(LoggedOutState)  # Default state

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


class PlaceHolderUser(User):  # TODO: Refactorizar para permitir no tener un usuario

    def __init__(self):
        super().__init__()


class Student(User):
    user_type = UserTypeEnum.student

    def __init__(self, user_in: UserModel):
        super().__init__()
        # TODO base state in UserModel
        user_in = user_in.dict()
        self.id = user_in["id"]
        self.first_name = user_in["first_name"]
        self.last_name = user_in["last_name"]
        self.email = user_in["email"]
        self.password = user_in["password"]


class Professor(User):
    user_type = UserTypeEnum.professor

    def __init__(self, user_in: UserModel):
        super().__init__()
        user_in = user_in.dict()
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
    def createUser(self, user_in: UserModel):
        pass

    async def registerUser(self, db: Database, user: UserIn) -> dict:
        # new_user = self.createUser(user)
        # TODO Validations might be done with pydantic validators
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
        if await UserModel.find_one({"email": user.email}):
            raise HTTPException(
                status_code=400, detail="This email already exists")

        auth_handler = AuthHandler()
        user.password = auth_handler.hash_password(user.password)
        new_user = await UserModel(**user.dict()).insert()

        # id = db.user.insert_one(user).inserted_id
        id = new_user.id
        token = auth_handler.encode_token(str(id))
        return {'token': token}


class StudentCreator(UserCreatorBlueprint):

    def createUser(self, user_in: UserModel) -> User:
        return Student(user_in)


class ProfessorCreator(UserCreatorBlueprint):

    def createUser(self, user_in: UserModel) -> User:
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
        return templates.TemplateResponse("index.html", {"request": request})

    def goToRegister(self, request):
        return templates.TemplateResponse("registration.html", {"request": request})

    def goToDashboard(self, request, context={}):
        return RedirectResponse("/")

    def goToNewProject(self, request):
        pass
