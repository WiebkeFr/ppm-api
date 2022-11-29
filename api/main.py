from typing import Union
from fastapi import Request, FastAPI
import pandas as pd
import json
import csv
import os.path

app = FastAPI()

@app.get("/")
def read_root():
    return {"ppm-api": "is running..."}

@app.post("/")
async def log(request: Request):
    body_as_byte = await request.body()
    all_infos = body_as_byte.decode('UTF-8').split("\r\n")
    body_as_string = [param for param in all_infos if param.startswith("{") and param.endswith("}")][0]
    body = json.loads(body_as_string)
    file_name = body['instance-name']
    print(file_name)
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
