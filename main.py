import os

import click as click
import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI
from matplotlib import pyplot as plt
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import upload, evaluate, train, frontend

tags_metadata = [
    {
        "name": "API – Upload",
        "description": "Routes to upload event-logs",
    },
    {
        "name": "API – Training",
        "description": "Routes to start training of selected model and ",
    },
    {
        "name": "API – Evaluation",
        "description": "Routes to evaluate complexity event-logs and accuracies of trained model",
    },
    {
        "name": "API – Prediction",
        "description": "Route to predict next event of uploaded process",
    },
    {
        "name": "Frontend",
        "description": "Pages to visualize the API routes",
    },
]

app = FastAPI(
    title="Predictive Process Monitoring - Next Event Prediction",
    version="1.0.0",
    contact={
        "name": "Wiebke Freitag",
        "email": "wiebke.freitag@tum.de",
    },
    openapi_tags=tags_metadata
)

port = os.environ["PORT"] if os.environ["PORT"] else "9999"
base_path = f"/ports/{port}"

print(base_path)

app.include_router(upload.router,
                   prefix=base_path + "/api/upload",
                   tags=["API – Upload"])

app.include_router(evaluate.router,
                   prefix=base_path + "/api/evaluate",
                   tags=["API – Evaluation"])

app.include_router(train.router,
                   prefix=base_path + "/api/train",
                   tags=["API – Training"])

app.include_router(train.router,
                   prefix=base_path + "/api/predict",
                   tags=["API – Prediction"])

app.include_router(frontend.router,
                   prefix=base_path,
                   tags=["API – Frontend"])

@app.get("/test", tags=["API – Organization"])
async def get_training_history_image(request: Request):
    return {"state": "success"}


@app.delete("/api/delete/{dir}", tags=["API – Organization"])
async def delete_files_in_directory(dir: str):
    if os.path.isdir(f"data/{dir}"):
        if len(os.listdir(f"data/{dir}")) == 0:
            return {"status": "directory is already empty"}
        for file in os.listdir(f"data/{dir}"):
            os.remove(f"data/{dir}/{file}")
        return {"status": "files removed successfully"}
    else:
        return {"status": "provided directory does not exist"}

app.mount(base_path + "/static", StaticFiles(directory="frontend/build/static"), name="static")
app.mount(base_path + "/public", StaticFiles(directory="frontend/public"), name="build")

@click.command()
@click.option('-p', '--port', type=click.IntRange(min=9000, max=10000), default=9999, help='The port on which the webservice is running')
def main(port):
    os.environ["PORT"] = str(port)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, root_path=f"/ports/9999", reload=True)


if __name__ == '__main__':
    main()
