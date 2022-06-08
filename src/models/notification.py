from beanie import Document
from bson import ObjectId
from pydantic import BaseModel
from typing import Any, Optional, List
from models.user import UserModel, UserOut
from datetime import date
from beanie import Document, Link, PydanticObjectId

class NotificationIn(BaseModel):
    sent_by: PydanticObjectId
    received_by: PydanticObjectId
    description: str
    viewed: bool = False

class NotificationOut(BaseModel):
    id: PydanticObjectId
    sent_by: UserOut
    received_by: UserOut
    description: str
    viewed: bool = False


class NotificationModel(Document, NotificationOut):
    sent_by: Link[UserModel]
    received_by: Link[UserModel]
    description: str
    viewed: bool = False

    class Settings:
        name = 'notifications'
        bson_encoders = {
            date: lambda dt: datetime(
                year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0, second=0)
        }

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
