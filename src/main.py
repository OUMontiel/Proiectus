import imp
from fastapi import FastAPI, Request, Depends, Cookie
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from mongoengine import connect, get_db
from routes.user import user
from config.db import db
from utils.auth import AuthHandler
from typing import Union
from bson import ObjectId
import os

load_dotenv('.env')

app = FastAPI()
auth_handler = AuthHandler()

# TODO (Alam) Verificar si hacer la conexión aquí es seguro
# connection = connect(host=os.environ['MONGODB_URI'])

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# @app.on_event("startup")
# async def create_db_client():
#     # Prueba de conexión a Mongo
#     print(get_db())
#     return

app.include_router(user)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
@app.get("/register", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def index(request: Request, token: Union[str, None] = Cookie(default=None)):
    user_id = None
    try:
        user_id = ObjectId(auth_handler.auth_wrapper(token))
    except:
        return RedirectResponse("/")

    if (db.user.find_one({"_id": user_id})):
        return templates.TemplateResponse("dashboard.html", {"request": request})
    else:
        return RedirectResponse("/")


'''
user_id = Depends(auth_handler.auth_wrapper)

@app.get("/example/{id}", response_class=HTMLResponse)
def example(request: Request, id: str):
    return templates.TemplateResponse("example.html", {"request": request, "id": id})
'''
