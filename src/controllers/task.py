from abc import ABC, abstractmethod
from typing import List
from beanie import PydanticObjectId
from beanie.operators import In, NotIn, AddToSet

from bson import ObjectId

from models.project import ProjectIn, ProjectModel
from models.task import TaskIn, TaskOut, TaskModel
from config.db import db

from controllers.user import PyMongoUsersController
from models.user import UserModel

users_controller = PyMongoUsersController()


class TasksController(ABC):

    @abstractmethod
    async def get_task(self, id: str) -> TaskModel:
        return NotImplementedError()

    @abstractmethod
    async def get_tasks_by_ids(self, ids: List[str]) -> List[TaskModel]:
        return NotImplementedError()

    @abstractmethod
    async def create_task(self, data: TaskModel) -> None:
        return NotImplementedError()


class PyMongoTasksController(TasksController):

    async def get_task(self, id: str) -> TaskModel:
        task = await TaskModel.get(ObjectId(id), fetch_links=True)
        return task

    async def get_tasks_by_ids(self, ids: List[str]) -> List[TaskModel]:
        return NotImplementedError()

    async def create_task(self, data: TaskIn) -> None:
        admin = await UserModel.get(data.admin)
        assert admin is not None, f'Admin with id ({data.admin}) not found'

        members = await UserModel.find_many(In(UserModel.id, data.members)).to_list()

        project_values = data.dict()
        del project_values['admin']
        del project_values['members']

        project = ProjectModel(
            **project_values, invitees=[], admin=admin, members=members)
        await project.create()