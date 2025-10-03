import os
from fastapi import FastAPI, Request, UploadFile, Form, Depends
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from passlib.hash import bcrypt
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()
PASSWORD = os.getenv("APP_PASSWORD", "changeme")
SECRET_KEY = os.getenv("SECRET_KEY", Fernet.generate_key().decode())

fernet = Fernet(SECRET_KEY.encode() if isinstance(SECRET_KEY,str) else SECRET_KEY)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DB_PATH = "database.db"

# Crear tabla si no existe
with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY, filename TEXT, data BLOB)")
    conn.commit()

def check_password(password: str):
    return password == PASSWORD

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, password: str = Form(...)):
    if not check_password(password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Contraseña incorrecta"})
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="auth", value="ok")
    return response

def auth_required(request: Request):
    if request.cookies.get("auth") != "ok":
        return False
    return True

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not auth_required(request):
        return RedirectResponse(url="/")
    with sqlite3.connect(DB_PATH) as conn:
        files = conn.execute("SELECT id, filename FROM files").fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "files": files})

@app.post("/upload")
async def upload(request: Request, file: UploadFile = None):
    if not auth_required(request):
        return RedirectResponse(url="/")
    if file:
        data = await file.read()
        enc = fernet.encrypt(data)
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO files(filename,data) VALUES(?,?)", (file.filename, enc))
            conn.commit()
    return RedirectResponse(url="/dashboard")

@app.get("/download/{file_id}")
async def download(request: Request, file_id: int):
    if not auth_required(request):
        return RedirectResponse(url="/")
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT filename, data FROM files WHERE id=?", (file_id,)).fetchone()
    if row:
        filename, enc = row
        data = fernet.decrypt(enc)
        path = f"/tmp/{filename}"
        with open(path, "wb") as f:
            f.write(data)
        return FileResponse(path, filename=filename)
    return RedirectResponse(url="/dashboard")

@app.get("/delete_all")
async def delete_all(request: Request):
    if not auth_required(request):
        return RedirectResponse(url="/")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM files")
        conn.commit()
    return RedirectResponse(url="/dashboard")
