from beanie import Document, Link, PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List
from datetime import date, datetime

from models.user import UserOut, UserModel


class ProjectIn(BaseModel):
    title: str
    description: str  # TODO Update to datetime
    due_date: date
    admin: PydanticObjectId  # admin _id
    members: List[PydanticObjectId]  # list of _id


class ProjectOut(ProjectIn):
    id: PydanticObjectId
    admin: UserOut
    members: List[UserOut]
    invitees: List[UserOut]

    class Config:
        allow_population_by_field_name = True


class ProjectModel(Document, ProjectOut):
    admin: Link[UserModel]
    members: List[Link[UserModel]]
    invitees: List[Link[UserModel]] = []  # Refs to User

    class Settings:
        name = 'projects'
        bson_encoders = {
            date: lambda dt: datetime(
                year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0, second=0)
        }

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


ProjectModel.update_forward_refs()
