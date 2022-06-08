
from beanie import PydanticObjectId
from beanie.operators import NotIn
from bson import ObjectId
from config.db import db
from fastapi import APIRouter, Response, status, Request, Cookie, Body
from models.feedback import FeedbackIn
from models.project import ProjectIn
from models.task import TaskIn, TaskModel
from models.user import UserModel, UserOut
from schemas.project import projectEntity
from starlette.status import HTTP_204_NO_CONTENT
from typing import Any, List
from config.controllers import projects_controller, users_controller, notifications_controller
from utils.auth import AuthHandler
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Union
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
project = APIRouter(prefix='/projects')
auth_handler = AuthHandler()


@project.get("/create", response_class=HTMLResponse)
async def index(request: Request, token: Union[str, None] = Cookie(default=None)):
    possible_users = await UserModel\
        .find(NotIn(UserModel.id, [ObjectId(request.state.user.id)]), fetch_links=True)\
        .project(UserOut)\
        .to_list()

    # TODO Implement User GoToNewProject to Handle UserState
    return templates.TemplateResponse("createProject.html",
                                      {
                                          "request": request,
                                          "user": request.state.user,
                                          "possible_users": possible_users
                                      })

@project.get('/{id}', response_class=HTMLResponse)
async def find_project(request: Request, id: PydanticObjectId):
    project = await projects_controller.get_project(id)
    tasks = await projects_controller.get_all_tasks()
    feedback = await projects_controller.get_feedback(id)

    return templates.TemplateResponse("project.html",
                                      {
                                          "request": request,
                                          "user": request.state.user,
                                          "project": project,
                                          "tasks": tasks,
                                          "feedback": feedback
                                      })

@project.get('/{id}/createTask', response_class=HTMLResponse)
async def find_project(request: Request, id: PydanticObjectId):
    project = await projects_controller.get_project(id)

    return templates.TemplateResponse("createTask.html",
                                      {
                                          "request": request,
                                          "user": request.state.user,
                                          "project": project
                                      })

@project.get('/task/{id}', response_class=HTMLResponse)
async def find_project(request: Request, id: PydanticObjectId):
    task = await projects_controller.get_task(id)
    users = await projects_controller.get_all_users()

    return templates.TemplateResponse("task.html",
                                      {
                                          "request": request,
                                          "user": request.state.user,
                                          "task": task,
                                          "users": users
                                      })

@project.post('/create')
async def create_project(project: ProjectIn = Body(...)):
    await projects_controller.create_project(project)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Project created")

@project.post('/createTask')
async def create_task(task: TaskIn = Body(...)):
    #print(task)
    #print(TaskIn(**task))
    await projects_controller.create_task(task)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Task created")


@project.post('/invite/{id}')
async def invite_to_project(id: PydanticObjectId, invitees: List[str] = Body(...)):
    await projects_controller.invite_by_email(id, invitees)
    return Response(status_code=HTTP_204_NO_CONTENT)


@project.get('/accept/{id}')
async def accept_invite(request: Request, id: PydanticObjectId):
    await users_controller.accept_project_invitation(request.state.user.id, id)
    await notifications_controller.notify_all(request.state.user.id, id)
    return Response(status_code=HTTP_204_NO_CONTENT)

@project.post('/{id}/feedback')
async def invite_to_project(id: PydanticObjectId, feedback: FeedbackIn = Body(...)):
    await projects_controller.add_feedback(id, feedback)
    return Response(status_code=HTTP_204_NO_CONTENT)

# TODO Verify that it works
@project.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["projects"])
def delete_user(id: str):
    projectEntity(db.projects.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)
