from beanie import Document
from bson import ObjectId
from pydantic import BaseModel
from typing import Any, Optional, List
from models.user import UserModel
from datetime import date, datetime


class NotificationModel(Document, BaseModel):
    id: Optional[str]
    sent_by: str
    received_by: str
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
