from typing import Optional
import jwt
import os

from bson import ObjectId
from datetime import datetime, timedelta
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from pymongo.database import Database

from config.controllers import users_controller
from models.user import UserModel

class UserAuth(BaseModel):
    '''Campos del usuario que son recibidos por autenticación (log in)'''
    email: EmailStr
    password: str
    
class AuthHandler():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = os.environ['SECRET_JWT']

    def hash_password(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_pw, hashed_pw):
        return self.pwd_context.verify(plain_pw, hashed_pw)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }

        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def auth_login(self, db: Database, auth: UserAuth) -> dict:
        # Required fields
        if (not auth.email or not auth.password):
            raise HTTPException(status_code=400, detail="Missing fields.")

        # Validate email
        try:
            auth.email = auth.email.lower()
            auth.email = validate_email(auth.email).email
        except EmailNotValidError as e:
            raise HTTPException(status_code=401, detail="Invalid email and/or password.")
        
        userDB = db.user.find_one({ "email": auth.email })
        if (not userDB or not self.verify_password(auth.password, userDB["password"])):
            raise HTTPException(status_code=401, detail="Invalid email and/or password")

        token = self.encode_token(str(userDB["_id"]))
        return { 'token': token }

    async def auth_is_logged_in(self, db: Database, token: str) -> Optional[UserModel]:
        try:
            user_id = ObjectId(self.decode_token(token))
            return await users_controller.get_user(user_id)
        except:
            return False