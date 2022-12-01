from fastapi import FastAPI
import pandas as pd
import json
import csv
import os.path
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class = HTMLResponse, tags=["Frontend"])
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/upload", tags=["API"])
async def upload(request: Request):
    form = await request.form()
    print(form)
    return {"state": "success"}


@app.post("/api/log", tags=["API"])
async def log(request: Request):
    body_as_byte = await request.body()
    all_infos = body_as_byte.decode('UTF-8').split("\r\n")
    body_as_string = [param for param in all_infos if param.startswith("{") and param.endswith("}")][0]
    body = json.loads(body_as_string)
    file_name = body['instance-name']
    file_exists = os.path.exists('{0}.csv'.format(file_name))
    if file_exists:
        with open('{0}.csv'.format(file_name), 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(list(body.values()))
    else:
        with open('{0}.csv'.format(file_name), 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(list(body.keys()))
            writer.writerow(list(body.values()))

    df = pd.read_csv('{0}.csv'.format(file_name))
    print(df)

    return {"trace": "success"}
