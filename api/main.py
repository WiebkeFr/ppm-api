from typing import Union
from fastapi import Request, FastAPI
import json

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
    print(body)
    return {"item_id": "success"}
