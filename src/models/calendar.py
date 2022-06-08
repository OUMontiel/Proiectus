from unicodedata import name
from beanie import Document, Link, PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Any, Optional, List
from datetime import date, datetime

from models.user import UserOut, UserModel

class CalendarModel(BaseModel):
    user_id = str
    available_times = [datetime]

    class Settings:
        name = 'calendars'
        bson_encoders = {
            date: lambda dt: datetime(year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0, second=0)
        }

    @classmethod
    def from_mongo_doc(cls, doc: Any) -> 'CalendarModel':
        instance = CalendarModel(
            id=str(doc['_id']),
            title=doc['title'],
            description=doc['description'],
            due_date=doc['due_date'],
            admin=doc['admin'],
            members=doc['members'],
            invitees=doc.get('invitees') or []
        )
        return instance
