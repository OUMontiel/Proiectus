from bson import ObjectId
from config.db import db
from fastapi import APIRouter, Response, status, Request, Cookie, Body
from typing import List
from utils.auth import AuthHandler
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.notification import NotificationModel
from schemas.notification import *

notification = APIRouter()
auth_handler = AuthHandler()


@notification.get('/notifications/{id}', response_model=List[NotificationModel])
async def find_user_active_notifications(request: Request, id: str):
    return notificationsEntity(db.notifications.find(), id)



@notification.post('/notifications/create')
async def create_notification(notification: NotificationModel = Body(...)):
    notification = jsonable_encoder(notification)
    new_notification = db.notifications.insert_one(notification)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="created notification")


@notification.put('/notifications/deactivate/{id}', response_model=NotificationModel, tags=["notifications"])
def update_notification(id: str, notification: NotificationModel):
    db.notifications.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(notification)})
    return notificationEntity(db.notifications.find_one({"_id": ObjectId(id)}))