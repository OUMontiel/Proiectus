from abc import ABC, abstractmethod
from turtle import update
from typing import Any, List
from beanie import PydanticObjectId
from beanie.operators import Push, Pull
from bson import ObjectId


from config.db import db
from models.user import UserBase, UserIn, UserModel
from models.project import ProjectModel
from schemas.project import projectEntity
from models.notification import NotificationModel
from schemas.notification import *


class UsersController(ABC):

    @abstractmethod
    async def get_user(self, id: str) -> UserModel:
        return NotImplementedError()

    @abstractmethod
    async def get_users_by_ids(self, ids: List[str]) -> List[UserModel]:
        return NotImplementedError()

    @abstractmethod
    async def create_user(self, data: UserModel) -> None:
        return NotImplementedError()

    @abstractmethod
    async def delete_by_ids(self, ids: List[str]) -> None:
        return NotImplementedError()

    @abstractmethod
    async def update_user(self, id: str, data: UserModel) -> None:
        return NotImplementedError()

    async def get_project_invitations(self, id: str) -> List[ProjectModel]:
        return NotImplementedError()

    async def get_project_memberships(self, id: str) -> List[ProjectModel]:
        return NotImplementedError()

    async def get_user_notifications(self, id: str) -> List[NotificationModel]:
        return NotImplementedError()

    @abstractmethod
    async def decline_project_invitation(self, id: str) -> List[str]:
        pass

    @abstractmethod
    async def accept_project_invitation(self, id: str) -> List[str]:
        pass

    @abstractmethod
    async def update_notifications(self, id: str):
        pass


class PyMongoUsersController(UsersController):

    async def get_user(self, id: PydanticObjectId) -> UserModel:
        return await UserModel.get(id)

    async def get_users_by_ids(self, ids: List[str]) -> List[UserModel]:
        return NotImplementedError()

    async def create_user(self, data: UserBase) -> None:
        return NotImplementedError()

    async def delete_by_ids(self, ids: List[str]) -> None:
        return NotImplementedError()

    async def update_user(self, id: str, data: UserModel) -> None:
        db.user.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": dict(data)})

    async def get_project_invitations(self, id: PydanticObjectId) -> List[ProjectModel]:
        invited_projects = await ProjectModel.find(ProjectModel.invitees._id == ObjectId(id), fetch_links=True).to_list()
        return invited_projects

    async def get_project_memberships(self, id: PydanticObjectId) -> List[ProjectModel]:
        project_memberships = await ProjectModel.find(ProjectModel.members._id == ObjectId(id), fetch_links=True).to_list()
        return project_memberships

    async def get_user_notifications(self, id: str) -> List[NotificationModel]:
        user_notifs = notificationsEntity(db.notifications.find(), id)
        for notif in user_notifs:
            print(notif)
            db.notifications.find_one_and_update(
                {"_id": ObjectId(notif['id'])}, {"$set": {'viewed': True}})
        return user_notifs

    async def decline_project_invitation(self, id: str) -> List[str]:
        return NotImplementedError()

    async def accept_project_invitation(self, id: str, project_id: PydanticObjectId) -> List[str]:
        user = await self.get_user(id)
        mod = await ProjectModel\
            .find_one(ProjectModel.id == ObjectId(project_id))\
            .update(Push({
                'members': user.to_ref()}
            ))\
            .update(Pull({
                'invitees': user.to_ref()
            }))
        

    async def update_notifications(self, id, user_sending_id, project):
        user_sending = await self.get_user(user_sending_id)
        desc = "{} se ha unido al proyecto {}".format(
            str(user_sending.first_name), str(project.title))
        notification = NotificationModel(sent_by=user_sending_id,
                                         received_by=id,
                                         description=desc)
        print(notification)
        new_notification = db.notifications.insert_one(dict(notification))
