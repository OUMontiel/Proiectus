from pydantic import BaseModel
from pymongo.database import Database
from typing import Optional, List
from utils.auth import AuthHandler
from fastapi import HTTPException
from models.user import User, UserModel
from datetime import date


class ProjectModel(BaseModel):
    id: Optional[str]
    title: str
    description: str
    due_date: date
    admin: UserModel
    members: List[UserModel]

