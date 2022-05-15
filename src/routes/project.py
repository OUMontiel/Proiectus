from bson import ObjectId
from config.db import db
from fastapi import APIRouter, Response, status, Request, Cookie, Body
from models.project import ProjectModel
from models.user import UserTypeEnum
from schemas.project import projectEntity, projectsEntity
from starlette.status import HTTP_204_NO_CONTENT
from typing import List
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
    is_logged_in = await auth_handler.auth_is_logged_in(db, token)
    if not is_logged_in and (is_logged_in.user_type != UserTypeEnum.professor):
        return RedirectResponse("/dashboard")

    return templates.TemplateResponse("createProject.html", {"request": request, "user": is_logged_in, "possible_users": usersEntity(db.user.find())})
    

@project.get('/projects/{id}', response_model=ProjectModel)
async def find_project(id: str):
    return projectEntity(db.projects.find_one({"_id": ObjectId(id)}))

@project.post('/projects/create')
async def create_project(project: ProjectModel = Body(...)):
    print(project)
    project = jsonable_encoder(project)
    print(project)
    new_project = db.projects.insert_one(project)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="created project")

# TODO Verify that it works
@project.delete('/projects/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["projects"])
def delete_user(id: str):
    projectEntity(db.projects.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)
