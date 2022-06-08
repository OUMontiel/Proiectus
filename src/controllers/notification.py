from abc import ABC, abstractmethod
from typing import List
from beanie import PydanticObjectId
from beanie.operators import In, NotIn, AddToSet

from bson import ObjectId

from models.project import ProjectIn, ProjectModel
from config.db import db

from controllers.user import PyMongoUsersController
from controllers.project import PyMongoProjectsController
from models.user import UserModel

users_controller = PyMongoUsersController()
projects_controller = PyMongoProjectsController()

class NotificationsController(ABC):

    @abstractmethod
    async def notify_all(self, id, project_id):
        return NotImplementedError()


class PyMongoNotificationsController(NotificationsController):
  # Observer method
    async def notify_all(self, u_id: str, project_id: str, *args):
        project = await projects_controller.get_project(project_id)
        member_ids = [str(member.id) for member in project.members]
        for i in member_ids:
            if str(i) != str(u_id):
                user_sending = await users_controller.get_user(u_id)
                desc = "{} {} se ha unido al proyecto {}".format(
                    str(user_sending.first_name), str(user_sending.last_name), str(project.title))
                print(desc)

                await users_controller.update_notifications(i, u_id, desc)
                
        print("Finished sending notifications")
