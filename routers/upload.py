import pandas as pd
import csv
import os.path
from starlette.requests import Request
import xmltodict
import json
from fastapi import APIRouter, Response, BackgroundTasks
import uuid
import pm4py
from typing import Optional
from fastapi import Form, File, UploadFile
from pydantic import BaseModel
from helper.process_uploads import process_csv, process_xes
from utils.subscriptions import add_subscription
from utils.run_events import start_shell_script

router = APIRouter()


class Info(BaseModel):
    isWithHeader: bool
    delimiter: str
    caseIdColumn: int
    activityColumn: int
    timestampColumn: int


def remove_starting_event(filename: str):
    filepath = os.path.join(os.curdir, "data", "logs", filename)
    log = pm4py.read_xes(filepath)
    if "lifecycle:transition" in log:
        x = log[(log["lifecycle:transition"] == "complete") | (log["lifecycle:transition"] == "COMPLETE")]
        print(x[:3])
        print(x.columns)
        pm4py.write_xes(x[["concept:name", "time:timestamp", "case:concept:name"]], filepath)


@router.post("/event-logs")
async def upload_event_logs(response: Response, background_tasks: BackgroundTasks, file: UploadFile = File(...),
                            info: Optional[str] = Form(None)):
    print(file.filename)
    session_id = str(uuid.uuid4())

    if file.filename[-3:] == 'csv':
        process_csv(file, session_id, info)
    if file.filename[-3:] == 'xes':
        await process_xes(file, session_id)

    filename = "{}.{}".format(session_id, file.filename[-3:])
    response.set_cookie(key="ppm-api", value=filename)
    background_tasks.add_task(remove_starting_event, filename)
    return {"state": "success"}


@router.post("/cpee-process")
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


@router.post("/link")
async def upload_cpee_link(request: Request):
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


@router.post("/log")
async def collect_cpee_event_logs(request: Request):
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

    return {"state": "success"}
