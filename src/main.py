import imp
import os

from config.db import db
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mongoengine import connect, get_db
from routes.user import user
from typing import Union
from utils.auth import AuthHandler

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
async def index(request: Request, token: Union[str, None] = Cookie(default=None)):
    is_logged_in = await auth_handler.auth_is_logged_in(db, token)
    if is_logged_in:
        return RedirectResponse("/dashboard")
    
    return templates.TemplateResponse("index.html", {"request": request})
    
    
@app.get("/register", response_class=HTMLResponse)
async def index(request: Request, token: Union[str, None] = Cookie(default=None)):
    is_logged_in = await auth_handler.auth_is_logged_in(db, token)
    if is_logged_in:
        return RedirectResponse("/dashboard")

    return templates.TemplateResponse("registration.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def index(request: Request, token: Union[str, None] = Cookie(default=None)):
    is_logged_in = await auth_handler.auth_is_logged_in(db, token)
    if not is_logged_in:
        return RedirectResponse("/")

    return templates.TemplateResponse("dashboard.html", {"request": request})

'''
@app.get("/example/{id}", response_class=HTMLResponse)
def example(request: Request, id: str):
    return templates.TemplateResponse("example.html", {"request": request, "id": id})
'''
