from bson import ObjectId
from config.db import db
from fastapi import APIRouter, Response, status
from models.user import UserIn, UserOut, StudentCreator, ProfessorCreator, UserTypeEnum
from schemas.user import userEntity, usersEntity
from starlette.status import HTTP_204_NO_CONTENT
from typing import List
from utils.auth import AuthHandler, AuthDetails

user = APIRouter()
auth_handler = AuthHandler()

@user.get('/users', response_model=List[UserOut])
async def find_all_users():
    return usersEntity(db.user.find())

@user.post('/users/register')
async def create_user(user: UserIn):
    if (user.user_type == UserTypeEnum.professor):
        factory = ProfessorCreator()
        return await factory.registerUser(db, user)
    else:
        # Default is student
        factory = StudentCreator()
        return await factory.registerUser(db, user)

@user.post('/users/login')
async def login_user(auth: AuthDetails):
    return await auth_handler.auth_login(db, auth)

@user.get('/users/{id}', response_model=UserOut)
async def find_user(id: str):
    return userEntity(db.user.find_one({"_id": ObjectId(id)}))

# TODO Verify that it works
@user.put('/users/{id}', response_model=UserIn, tags=["users"])
def update_user(id: str, user: UserIn):
    db.user.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(user)})
    return userEntity(db.user.find_one({"_id": ObjectId(id)}))

# TODO Verify that it works
@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
    userEntity(db.user.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)
