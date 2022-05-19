from beanie import PydanticObjectId
from bson import ObjectId
import pydantic
from config.db import db
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

@user.get('/', response_model=List[UserOut])
async def find_all_users():
    return usersEntity(db.user.find())

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

@user.get('/{id}', response_model=UserOut)
async def find_user(id: PydanticObjectId):
    return await UserModel.get(id)

# TODO Verify that it works
@user.put('/{id}', response_model=UserOut, tags=["users"])
async def update_user(id: PydanticObjectId, user: UserBase):
    user = await UserModel.find_one(UserModel.id == id).update({"$set": dict(user)})
    return user

# TODO Verify that it works
@user.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
    userEntity(db.user.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)
