from abc import ABC, abstractmethod
from typing import List

from bson import ObjectId

from models.project import ProjectModel
from config.db import db

from controllers.user import PyMongoUsersController

users_controller = PyMongoUsersController()

class ProjectsController(ABC):

    @abstractmethod
    def get_project(self, id: str) -> ProjectModel:
        return NotImplementedError()

    @abstractmethod
    def get_projects_by_ids(self, ids: List[str]) -> List[ProjectModel]:
        return NotImplementedError()

    @abstractmethod
    def create_project(self, data: ProjectModel) -> None:
        return NotImplementedError()

    @abstractmethod
    def delete_by_ids(self, ids: List[str]) -> None:
        return NotImplementedError()

    @abstractmethod
    def update_project(self, id: str, data: ProjectModel) -> None:
        return NotImplementedError()

    @abstractmethod
    def get_possible_invitees(self, id: str) -> List[str]:
        return NotImplementedError()

    @abstractmethod
    def invite_to_project(self, id: str, invitees: List[str]) -> None:
        return NotImplementedError()

    @abstractmethod
    def notify_all(self, id):
        return NotImplementedError()


class PyMongoProjectsController(ProjectsController):

    def get_project(self, id: str) -> ProjectModel:
        mongo_instance = db.projects.find_one({'_id': ObjectId(id)})
        project = ProjectModel.from_mongo_doc(mongo_instance)
        return project

    def get_projects_by_ids(self, ids: List[str]) -> List[ProjectModel]:
        return NotImplementedError()

    def create_project(self, data: ProjectModel) -> None:
        return NotImplementedError()

    def delete_by_ids(self, ids: List[str]) -> None:
        return NotImplementedError()

    def update_project(self, id: str, data: ProjectModel) -> None:
        db.projects.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": dict(data)})

    def get_possible_invitees(self, id: str) -> List[str]:
        project = self.get_project(id)
        member_ids = [str(member.id) for member in project.members]
        possible_invitees = db.user.find(
            {'_id': {'$nin': member_ids}}, projection={'_id': 1})

        return [str(invitee['_id']) for invitee in list(possible_invitees)]

    def invite_to_project(self, id: str, invitees: List[str]) -> None:
        project = self.get_project(id)
        possible_invitees = set(self.get_possible_invitees(id))
        incoming_invitees = possible_invitees.intersection(set(invitees))
        new_invitees = list(set(project.invitees).union(incoming_invitees))
        
        db.projects.update_one({'_id': ObjectId(project.id)}, {
                               '$set': {'invitees': new_invitees}})

    def invite_by_email(self, id: str, invitee_emails: List[str]) -> None:
        invitees = db.user.find({
            'email': {'$in': invitee_emails}
        }, projection={'_id'})
        invitees = [str(invitee['_id']) for invitee in list(invitees)]

        self.invite_to_project(id, invitees)

    # Observer method
    def notify_all(self, u_id: str, project_id: str):
        project = self.get_project(project_id)
        member_ids = [str(member.id) for member in project.members]
        print(member_ids)
        for i in member_ids:
            if i != u_id:
                users_controller.update_notifications(i, u_id, project)
        print("Finished sending notifications")
