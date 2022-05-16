from bson import ObjectId
from pydantic import BaseModel
from typing import Any, Optional, List
from models.user import UserModel
from datetime import date


class NotificationModel(BaseModel):
    id: Optional[str]
    sent_by: str
    received_by: str
    description: str
    viewed: bool = False

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @classmethod
    def from_mongo_doc(cls, doc: Any) -> 'NotificationModel':
        instance = NotificationModel(
            id=str(doc['_id']),
            sent_by=doc['sent_by'],
            received_by=doc['received_by'],
            description=doc['description'],
            viewed=doc['viewed']
        )
        return instance

