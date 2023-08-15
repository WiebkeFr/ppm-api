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
from utils.process_uploads import process_csv, process_xes, process_xml
from utils.subscriptions import add_subscription
from utils.run_events import start_shell_script
import shutil
router = APIRouter()

TRACE_NUMBER = 50

def remove_starting_event(filename: str):
    filepath = os.path.join(os.curdir, "data", "logs", filename)
    log = pm4py.read_xes(filepath)
    if "lifecycle:transition" in log:
        x = log[(log["lifecycle:transition"] == "complete") | (log["lifecycle:transition"] == "COMPLETE")]
        pm4py.write_xes(x[["concept:name", "time:timestamp", "case:concept:name"]], filepath)


@router.post("/event-logs")
async def upload_event_logs(response: Response, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    print(file.filename)
    session_id = str(uuid.uuid4())

    if file.filename[-3:] == 'csv':
        process_csv(file, session_id)
    if file.filename[-3:] == 'xes':
        await process_xes(file, session_id)
    if file.filename[-3:] == 'xml':
        background_tasks.add_task(process_xml, file, session_id)

    type = "xes" if file.filename[-3:] == "xes" else "csv"
    filename = "{}.{}".format(session_id, type)
    response.set_cookie(key="ppm-api", value=filename)
    if type == "xes":
        background_tasks.add_task(remove_starting_event, filename)
    return {"state": "success"}


@router.post("/log")
async def collect_cpee_event_logs(request: Request):
    body_as_byte = await request.body()
    all_infos = body_as_byte.decode('UTF-8').split("\r\n")
    body_as_string = [param for param in all_infos if param.startswith("{") and param.endswith("}")][0]
    body = json.loads(body_as_string)

    id = body['instance-name']
    file_path = os.path.join(os.curdir, "data", "cpee", "{}.csv".format(id))
    progress_path = os.path.join(os.curdir, "data", "cpee", "{}_progress.txt".format(id))

    if body['topic'] == 'state' and body['content']["state"] == 'finished':
        print("FINISHED", body['instance'])
        if os.path.isfile(progress_path):
            with open(progress_path, 'w+') as f:
                old_state = f.read()
                print(old_state)
                new_state = int(old_state) + 1

                if new_state == TRACE_NUMBER:
                    print("FINISHED ALL")
                    shutil.move(file_path, f"/data/logs/{id}.csv")
                    os.remove(progress_path)
                    return {"state": "trace finished"}
                else:
                    f.write(str(new_state))
                    f.close()
        else:
            with open(progress_path, 'w') as f:
                print("START")
                f.write("PROGRESS")
                f.close()

    if body['name'] != 'done':
        return {"state": "activity called"}

    file_exists = os.path.exists(file_path)
    case_id = body['instance']
    time_stamp = body['timestamp']
    event_id = body['content']["activity"]

    if file_exists:
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([case_id, event_id, time_stamp])
    else:
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["case_id", "event_id", "time_stamp"])
            writer.writerow([case_id, event_id, time_stamp])

    df = pd.read_csv(file_path)
    print(df, df.columns)

    return {"state": "success"}
