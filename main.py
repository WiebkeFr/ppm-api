import os
import uvicorn
from fastapi import FastAPI
from matplotlib import pyplot as plt
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import upload, evaluate, train, frontend, internal

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
    {
        "name": "Internal",
        "description": "Internal routes to create multiple model for the bachelors thesis",
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

app.include_router(upload.router,
                   prefix="/api/upload",
                   tags=["API – Upload"])

app.include_router(evaluate.router,
                   prefix="/api/evaluate",
                   tags=["API – Evaluation"])

app.include_router(train.router,
                   prefix="/api/train",
                   tags=["API – Training"])

app.include_router(train.router,
                   prefix="/api/predict",
                   tags=["API – Prediction"])

app.include_router(frontend.router,
                   tags=["Frontend"])

app.include_router(internal.router,
                   prefix="/internal",
                   tags=["Internal"])


@app.get("/test", tags=["API – Organization"])
async def test(request: Request):
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

app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")
app.mount("/public", StaticFiles(directory="frontend/public"), name="build")

@click.command()
@click.option('-p', '--port', type=click.IntRange(min=9000, max=10000), default=9999, help='The port on which the webservice is running')
def main(port):
    os.environ["PORT"] = str(port)
    uvicorn.run("main:app", host="::1", port=9999, root_path=f"/ports/9999", reload=True)


if __name__ == '__main__':
    main()
