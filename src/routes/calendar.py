
from beanie import PydanticObjectId
from beanie.operators import NotIn
from bson import ObjectId
from config.db import db
from fastapi import APIRouter, Response, status, Request, Cookie, Body
from models.calendar import CalendarModel
from starlette.status import HTTP_204_NO_CONTENT
from typing import List
from utils.auth import AuthHandler
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Union
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
calendar = APIRouter(prefix='/calendar')
auth_handler = AuthHandler()


@calendar.get("/", response_class=HTMLResponse)
async def displayCalendar(request: Request, token: Union[str, None] = Cookie(default=None)):
    return templates.TemplateResponse("calendar.html",
                                      {
                                          "request": request,
                                          "user": request.state.user
                                      })
'''
@calendar.post('/')
async def create_notification(notification: CalendarModel = Body(...)):
    notification = jsonable_encoder(notification)
    new_notification = db.notifications.insert_one(notification)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="created notification")

@calendar.post('/')
async def addAvailableTimes(calendar: CalendarModel = Body(...)):
    await projects_controller.create_project(project)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Project created")
'''