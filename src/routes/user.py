from beanie import PydanticObjectId
from bson import ObjectId
import pydantic
from config.db import db
from config.controllers import users_controller
from fastapi import APIRouter, Response, status
from models.user import UserIn, UserModel, UserOut, UserTypeEnum
from utils.factories import StudentCreator, ProfessorCreator
from schemas.user import userEntity, usersEntity
from starlette.status import HTTP_204_NO_CONTENT
from typing import List
from models.user import UserBase
from utils.auth import AuthHandler, UserAuth

user = APIRouter(prefix='/users')
auth_handler = AuthHandler()

@user.get('/', response_model=List[UserOut], response_model_by_alias=False)
async def find_all_users():
    return await UserModel.all().to_list()

@user.post('/register')
async def create_user(user: UserIn):
    if (user.user_type == UserTypeEnum.professor):
        factory = ProfessorCreator()
        return await factory.registerUser(db, user)
    else:
        # Default is student
        factory = StudentCreator()
        return await factory.registerUser(db, user)

@user.post('/login')
async def login_user(auth: UserAuth):
    return await auth_handler.auth_login(db, auth)

@user.get('/{id}', response_model=UserOut, response_model_by_alias=False)
async def find_user(id: PydanticObjectId):
    return await users_controller.get_user(id)

# TODO Verify that it works
@user.put('/{id}', response_model=UserOut, tags=["users"], response_model_by_alias=False)
async def update_user(id: PydanticObjectId, user: UserBase):
    await users_controller.update_user(id, user)
    return user

# TODO Verify that it works
@user.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(id: PydanticObjectId):
    await users_controller.delete(id)
    return Response(status_code=HTTP_204_NO_CONTENT)
