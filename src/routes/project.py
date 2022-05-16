from bson import ObjectId
from config.db import db
from fastapi import APIRouter, Response, status, Request, Cookie, Body
from models.project import ProjectModel
from models.user import UserTypeEnum
from schemas.project import projectEntity, projectsEntity
from starlette.status import HTTP_204_NO_CONTENT
from typing import List
from config.controllers import projects_controller, users_controller
from utils.auth import AuthHandler, AuthDetails
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from typing import Union
from fastapi.templating import Jinja2Templates
from schemas.user import userEntity, usersEntity
from fastapi.encoders import jsonable_encoder


templates = Jinja2Templates(directory="templates")
project = APIRouter()
auth_handler = AuthHandler()


@project.get("/projects/create", response_class=HTMLResponse)
async def index(request: Request, token: Union[str, None] = Cookie(default=None)):
    if request.state.user.user_type != UserTypeEnum.professor:
        return RedirectResponse("/dashboard")

    return templates.TemplateResponse("createProject.html",
                                      {
                                          "request": request,
                                          "user": request.state.user,
                                          "possible_users": usersEntity(db.user.find({'_id': {'$nin': [ObjectId(request.state.user.id)]}}))
                                      })


@project.get('/projects/{id}', response_model=ProjectModel)
async def find_project(request: Request, id: str):
    project = projectEntity(projects_controller.get_project(id))
    return templates.TemplateResponse("project.html",
                                      {
                                          "request": request,
                                          "user": request.state.user,
                                          "project": project
                                      })


@project.post('/projects/create')
async def create_project(project: ProjectModel = Body(...)):
    project = jsonable_encoder(project)
    new_project = db.projects.insert_one(project)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="created project")


@project.post('/projects/invite/{id}')
async def invite_to_project(id: str, invitees: List[str] = Body(...)):
    print(invitees)
    try:
        projects_controller.invite_by_email(id, invitees)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except:
        return Response(status_code=500)

@project.get('/projects/accept/{id}')
async def invite_to_project(request: Request, id: str):
    try:
        users_controller.accept_project_invitation(request.state.user.id, id)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as e: 
        print(e)
        return Response(status_code=500)


# TODO Verify that it works
@project.delete('/projects/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["projects"])
def delete_user(id: str):
    projectEntity(db.projects.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)
