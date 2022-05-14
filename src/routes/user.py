from bson import ObjectId
from fastapi import APIRouter, Response, status, HTTPException
from config.db import db
from models.user import User
from passlib.hash import sha256_crypt
from schemas.user import userEntity, usersEntity
from starlette.status import HTTP_204_NO_CONTENT
from email_validator import validate_email, EmailNotValidError
from utils.auth import AuthHandler

user = APIRouter()
auth_handler = AuthHandler()

@user.get('/users', response_model=User, tags=["users"])
def find_all_users():
    return usersEntity(db.user.find())

@user.post('/users/register')
async def create_user(user: User):
    new_user = dict(user)
    # Required fields
    if (not new_user["first_name"] or not new_user["last_name"]
        or not new_user["email"] or not new_user["password"]
        or not new_user["user_type"]):
        raise HTTPException(status_code=400, detail="Missing fields.")

    # Validate email
    try:
        new_user["email"] = new_user["email"].lower()
        new_user["email"] = validate_email(new_user["email"]).email
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail="Email is not valid.")

    # Check for duplicates
    if db.user.find_one({"email": new_user["email"]}):
        raise HTTPException(status_code=400, detail="This email already exists")

    new_user["password"] = auth_handler.hash_password(new_user["password"])
    del new_user["id"]
    
    id = db.user.insert_one(new_user).inserted_id
    token = auth_handler.encode_token(str(id))

    return { 'token': token }

@user.post('/users/login')
async def login_user(user: User):
    # Required fields
    if (not user["email"] or not user["password"]):
        raise HTTPException(status_code=400, detail="Missing fields.")

    userDB = db.user.find_one({ "email": user["email"] })
    if (not userDB or not auth_handler.verify_password(user["password"], userDB["password"])):
        raise HTTPException(status_code=401, detail="Invalid email and/or password")

    token = auth_handler.encode_token(userDB["id"])

    return { 'token': token }

@user.get('/users/{id}', response_model=User, tags=["users"])
def find_user(id: str):
    return userEntity(db.user.find_one({"_id": ObjectId(id)}))

@user.put('/users/{id}', response_model=User, tags=["users"])
def update_user(id: str, user: User):
    db.user.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(user)})
    return userEntity(db.user.find_one({"_id": ObjectId(id)}))

@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
    userEntity(db.user.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)
