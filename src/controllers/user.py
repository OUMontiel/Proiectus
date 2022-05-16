from abc import ABC, abstractmethod
from typing import Any, List

from bson import ObjectId


from config.db import db
from models.user import UserModel
from models.project import ProjectModel
from schemas.project import projectEntity
from models.notification import NotificationModel
from schemas.notification import *


class UsersController(ABC):

    @abstractmethod
    def get_user(self, id: str) -> UserModel:
        return NotImplementedError()

    @abstractmethod
    def get_users_by_ids(self, ids: List[str]) -> List[UserModel]:
        return NotImplementedError()

    @abstractmethod
    def create_user(self, data: UserModel) -> None:
        return NotImplementedError()

    @abstractmethod
    def delete_by_ids(self, ids: List[str]) -> None:
        return NotImplementedError()

    @abstractmethod
    def update_user(self, id: str, data: UserModel) -> None:
        return NotImplementedError()

    def get_project_invitations(self, id: str) -> List[ProjectModel]:
        return NotImplementedError()

    def get_project_memberships(self, id: str) -> List[ProjectModel]:
        return NotImplementedError()
    
    def get_user_notifications(self, id: str) -> List[NotificationModel]:
        return NotImplementedError()

    @abstractmethod
    def decline_project_invitation(self, id: str) -> List[str]:
        pass

    @abstractmethod
    def accept_project_invitation(self, id: str) -> List[str]:
        pass

    @abstractmethod
    def update_notifications(self, id:str):
        pass


class PyMongoUsersController(UsersController):

    def get_user(self, id: str) -> UserModel:
        mongo_instance = db.user.find_one({'_id': ObjectId(id)})
        user = UserModel.from_mongo_doc(mongo_instance)
        return user

    def get_users_by_ids(self, ids: List[str]) -> List[UserModel]:
        return NotImplementedError()

    def create_user(self, data: UserModel) -> None:
        return NotImplementedError()

    def delete_by_ids(self, ids: List[str]) -> None:
        return NotImplementedError()

    def update_user(self, id: str, data: UserModel) -> None:
        db.user.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": dict(data)})

    def get_project_invitations(self, id: str) -> List[ProjectModel]:
        invited_projects = db.projects.find(
            {'invitees': id})
        invited_projects = map(ProjectModel.from_mongo_doc, invited_projects)
        return list(invited_projects)

    def get_project_memberships(self, id: str) -> List[ProjectModel]:
        project_memberships = db.projects.find(
            {'members.id': id})
        project_memberships = map(
            ProjectModel.from_mongo_doc, project_memberships)
        return list(project_memberships)

    def get_user_notifications(self, id: str) -> List[NotificationModel]:
        user_notifs = notificationsEntity(db.notifications.find(), id)
        for notif in user_notifs:
            print(notif)
            db.notifications.find_one_and_update({"_id": ObjectId(notif['id'])}, {"$set": {'viewed': True}})
        return user_notifs

    def decline_project_invitation(self, id: str) -> List[str]:
        return NotImplementedError()

    def accept_project_invitation(self, id: str, project_id: str) -> List[str]:
        user = self.get_user(id)
        db.projects.find_one_and_update({'_id': ObjectId(project_id)}, {
            '$push': {
                'members': dict(user),
            },
            '$pull': {
                'invitees': id
            }
        })

    def update_notifications(self, id, user_sending_id, project):
        user_sending = self.get_user(user_sending_id)
        desc = "{} se ha unido al proyecto {}".format(str(user_sending.first_name), str(project.title))
        notification = NotificationModel(sent_by=user_sending_id,
                                        received_by=id,
                                        description=desc)
        print(notification)
        new_notification = db.notifications.insert_one(dict(notification))              

