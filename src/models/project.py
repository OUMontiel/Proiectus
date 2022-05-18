from bson import ObjectId
from pydantic import BaseModel
from typing import Any, Optional, List
from datetime import date

from models.user import UserOut
class ProjectModel(BaseModel):
    id: Optional[str]
    title: str
    description: str
    due_date: date
    admin: UserOut
    members: List[UserOut]
    invitees: List[str] = [] # Refs to User

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @classmethod
    def from_mongo_doc(cls, doc: Any) -> 'ProjectModel':
        instance = ProjectModel(
            id=str(doc['_id']),
            title=doc['title'],
            description=doc['description'],
            due_date=doc['due_date'],
            admin=doc['admin'],
            members=doc['members'],
            invitees=doc.get('invitees') or []
        )
        return instance

