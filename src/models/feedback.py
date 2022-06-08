from models.project import ProjectModel
from datetime import date, datetime
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel
from models.user import UserModel, UserOut


class FeedbackIn(BaseModel):
    content: str
    user: PydanticObjectId


class FeedbackModel(Document, FeedbackIn):
    date: datetime = datetime.now()
    project: 'Link[ProjectModel]'
    user: Link[UserModel]

    class Settings:
        name = 'feedback'
        bson_encoders = {
            date: lambda dt: datetime(
                year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0, second=0)
        }


FeedbackModel.update_forward_refs()
