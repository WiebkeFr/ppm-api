import pandas as pd
import csv
import os.path
from starlette.requests import Request
import xmltodict
import json
from fastapi import APIRouter
from typing import Annotated

from fastapi import FastAPI, Form, File, UploadFile

from utils.subscriptions import add_subscription
from utils.run_events import start_shell_script

router = APIRouter()


@router.post("/api/upload/event-logs", tags=["API"])
async def upload(file: UploadFile = File(...)):
    print("----------- EVENT UPLOAD ------------")
    print(file.filename)
    contents = await file.read()
    xml = contents.decode('UTF-8')
    print(xml)
    # file_name = file.filename
    # print(file_name)
    # add_subscription(xml)
    # updated_xml = add_subscription(xml)
    # with open(file_name, 'w') as file:
        # file.write(updated_xml)
        # file.close()
    # start_shell_script()
    return {"state": "success"}


@router.post("/api/upload/cpee-process", tags=["API"])
async def upload(request: Request):
    form_data = await request.form()
    file = form_data.get("file")
    contents = await file.read()
    xml = contents.decode('UTF-8')
    file_name = file.filename
    add_subscription(xml)
    updated_xml = add_subscription(xml)
    with open(file_name, 'w') as file:
        file.write(updated_xml)
        file.close()
    start_shell_script()
    return {"state": xmltodict.parse(updated_xml)}


@router.post("/api/upload/link", tags=["API"])
async def upload(request: Request):
    print("")
    form_data = await request.form()
    file = form_data.get("file")
    contents = await file.read()
    xml = contents.decode('UTF-8')
    file_name = file.filename
    add_subscription(xml)
    updated_xml = add_subscription(xml)
    with open(file_name, 'w') as file:
        file.write(updated_xml)
        file.close()
    start_shell_script()
    return {"state": xmltodict.parse(updated_xml)}


@router.post("/api/log", tags=["API"])
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
