from beanie import PydanticObjectId
from beanie.operators import NotIn
from bson import ObjectId
from config.db import db
from fastapi import APIRouter, Response, status, Request, Cookie, Body
from models.project import ProjectIn
from models.user import UserModel, UserOut
from models.task import TaskModel, TaskIn, TaskOut, TaskStatus
from schemas.project import projectEntity
from schemas.task import taskEntity
from starlette.status import HTTP_204_NO_CONTENT
from typing import List
from config.controllers import projects_controller, users_controller, tasks_controller
from utils.auth import AuthHandler
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Union
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
task = APIRouter(prefix='/task')
auth_handler = AuthHandler()

@task.get("/create", response_class=HTMLResponse)
async def index(request: Request, token: Union[str, None] = Cookie(default=None)):
    possible_users = await UserModel\
        .find(NotIn(UserModel.id, [ObjectId(request.state.user.id)]), fetch_links=True)\
        .task(UserOut)\
        .to_list()

    # TODO Implement User GoToNewProject to Handle UserState
    return templates.TemplateResponse("createTask.html",
                                      {
                                          "request": request,
                                          "user": request.state.user,
                                          "possible_users": possible_users
                                      })


@task.get('/{id}', response_class=HTMLResponse)
async def find_task(request: Request, id: PydanticObjectId):
    task = await tasks_controller.get_task(id)

    return templates.TemplateResponse("task.html",
                                      {
                                          "request": request,
                                          "user": request.state.user,
                                          "task": task
                                      })

@task.post('/create')
async def create_task(task: TaskIn = Body(...)):
    await tasks_controller.create_task(task)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Task created")