"""Punto de entrada de la aplicación FastAPI."""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import init_db
from .routers import persons, profiles, records

app = FastAPI(title="Base Centralizada de Datos Personales", version="0.1.0")

init_db()

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(persons.router)
app.include_router(records.router)
app.include_router(profiles.router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Página inicial con acceso rápido a la ficha unificada."""

    return templates.TemplateResponse("index.html", {"request": request})
