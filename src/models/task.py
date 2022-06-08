from enum import Enum
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel
from typing import List
from datetime import date, datetime
from models.project import ProjectModel

from models.user import UserOut, UserModel


class TaskStatus(str, Enum):
    about_to_start = 'About to start'
    in_progress = 'In progress'
    in_review = 'In review'
    finished = 'Finished'
    dropped = 'Dropped'


class TaskIn(BaseModel):
    title: str
    description: str
    due_date: date
    status: TaskStatus
    assignee: PydanticObjectId
    project: PydanticObjectId


class TaskOut(TaskIn):
    id: PydanticObjectId
    assignee: UserOut
    members: List[UserOut]
    invitees: List[UserOut]

    class Config:
        allow_population_by_field_name = True


class TaskModel(TaskOut, Document):
    assignee: Link[UserModel]
    project: Link[ProjectModel]

    class Settings:
        name = 'projects'
        bson_encoders = {
            date: lambda dt: datetime(
                year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0, second=0)
        }
