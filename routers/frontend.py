import os

from fastapi import APIRouter, Response, BackgroundTasks
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="frontend/build")

@router.get("/", response_class=HTMLResponse)
@router.get("/selection", response_class=HTMLResponse)
@router.get("/training", response_class=HTMLResponse)
@router.get("/prediction", response_class=HTMLResponse)
@router.get("/information", response_class=HTMLResponse)
def show_selected_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "prefix": f"ports/9999"})
