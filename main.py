import os

import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI
from matplotlib import pyplot as plt
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import upload, evaluate, train

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

@app.get("/test", tags=["API – Organization"])
async def get_training_history_image(request: Request):
    model_id = request.cookies.get('ppm-api').split(".")[0]

    plt.close()
    result_path = f"data/results/{model_id}_history.svg"
    history_path = f'data/training/{model_id}.csv'

    if not os.path.isfile(history_path):
        return

    df = pd.read_csv(history_path)

    print(df)

    labels = np.unique(df["Criterion"])
    ind = ind = np.arange(len(labels))

    columns = ['Accuracy', 'Precision', 'Recall']
    colors = ['blue', 'orange', 'green']
    width = 0.22

    fig, ax = plt.subplots()
    ax.set_xticks(ind + width, labels=labels)

    for index, (column, color) in enumerate(zip(columns, colors)):
        df_grouped = (
            df[['Criterion', column]].groupby(['Criterion'])
            .agg(['mean', 'std'])
        )
        df_grouped = df_grouped.droplevel(axis=1, level=0).reset_index()
        ax.bar(ind + index * width, df_grouped["mean"], width, yerr=df_grouped["std"], label=column)

    title = "Evaluation  of model in each criterion"
    plt.title(title, fontsize=13)
    plt.xlabel('Criterion', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.ylim(top=1.05)
    plt.grid(axis='y')
    plt.legend(loc='lower right')
    plt.savefig(result_path)
    plt.close()

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
templates = Jinja2Templates(directory="frontend/build")


@app.get("/", response_class=HTMLResponse, tags=["Frontend"])
@app.get("/selection", response_class=HTMLResponse, tags=["Frontend"])
@app.get("/training", response_class=HTMLResponse, tags=["Frontend"])
@app.get("/prediction", response_class=HTMLResponse, tags=["Frontend"])
@app.get("/information", response_class=HTMLResponse, tags=["Frontend"])
def show_selected_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

