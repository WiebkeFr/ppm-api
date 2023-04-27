from fastapi import FastAPI
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import api

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")
templates = Jinja2Templates(directory="frontend/build")

app.include_router(api.router)


@app.get("/{full_path:path}", response_class=HTMLResponse, tags=["Frontend"])
def show_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
