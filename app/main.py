import os
import csv
from fastapi import FastAPI, Request, Form, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from tinydb import TinyDB
from passlib.hash import bcrypt

from .auth import require_auth, is_authenticated

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.environ.get("SECRET_KEY", "secret"))

app.mount("/images", StaticFiles(directory="static/images"), name="images")

templates = Jinja2Templates(directory="templates")

db = TinyDB("db.json")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH", bcrypt.hash("changeme"))


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    if is_authenticated(request):
        return RedirectResponse("/dashboard")
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and bcrypt.verify(password, ADMIN_PASSWORD_HASH):
        request.session["user"] = username
        return RedirectResponse("/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)


@app.get("/dashboard", response_class=HTMLResponse, dependencies=[Depends(require_auth)])
async def dashboard(request: Request):
    records = db.all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "records": records})


@app.post("/upload", dependencies=[Depends(require_auth)])
async def upload(name: str = Form(...), notes: str = Form(""), file: UploadFile = File(...)):
    os.makedirs("static/images", exist_ok=True)
    file_location = os.path.join("static/images", file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    db.insert({"name": name, "notes": notes, "image": file.filename})
    return RedirectResponse("/dashboard", status_code=302)


@app.post("/upload_csv", dependencies=[Depends(require_auth)])
async def upload_csv(csv_file: UploadFile = File(...)):
    content = await csv_file.read()
    text = content.decode()
    reader = csv.DictReader(text.splitlines())
    for row in reader:
        db.insert(dict(row))
    return RedirectResponse("/dashboard", status_code=302)
