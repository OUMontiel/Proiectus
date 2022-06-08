from enum import Enum
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field
from typing import List
from datetime import date, datetime
from models.project import ProjectModel, ProjectOut

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
    projectID: PydanticObjectId


class TaskOut(TaskIn):
    id: PydanticObjectId = Field(alias='_id')
    assignee: UserOut
    projectID: ProjectOut

    class Config:
        allow_population_by_field_name = True


class TaskModel(Document, TaskOut):
    assignee: Link[UserModel]
    projectID: Link[ProjectModel]

    class Settings:
        name = 'task'
        bson_encoders = {
            date: lambda dt: datetime(
                year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0, second=0)
        }
