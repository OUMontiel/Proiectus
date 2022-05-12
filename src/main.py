import imp
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from mongoengine import connect, get_db
import os

load_dotenv('.env')

app = FastAPI()

# TODO (Alam) Verificar si hacer la conexión aquí es seguro
connection = connect(host=os.environ['MONGODB_URI'])

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def create_db_client():
    # Prueba de conexión a Mongo
    print(get_db())
    return

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/example/{id}", response_class=HTMLResponse)
def example(request: Request, id: str):
    return templates.TemplateResponse("example.html", {"request": request, "id": id})
