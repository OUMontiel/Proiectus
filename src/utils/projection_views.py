from ast import alias
from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class OnlyIdView(BaseModel):
    id: PydanticObjectId = Field(alias='_id')