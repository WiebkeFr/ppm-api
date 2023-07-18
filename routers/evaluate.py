import csv
import json

from fastapi import APIRouter, HTTPException
from starlette.requests import Request
import os

from starlette.responses import FileResponse

from evaluate_dataset.evaluate_dataset import event_log_assessment

router = APIRouter()


@router.get("/log")
async def evaluate_logs(request: Request):
    session_id = request.cookies.get('ppm-api')
    model_id = session_id.split(".")[0]
    path = f"data/evaluations/{model_id}.json"
    if os.path.isfile(path):
        with open(path) as f:
            return json.load(f)

    try:
        evaluation = event_log_assessment(session_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Dataset could not be read. Please upload it again!")

    eval_path = os.path.join(os.curdir, path)
    with open(eval_path, "w") as outfile:
        json.dump(evaluation, outfile)

    with open("RESULT/complexity.csv", "a") as stream:
        writer = csv.writer(stream)
        writer.writerow(["-", "-", "-", "-", *evaluation.values()])

    return evaluation


@router.get("/confusion-matrix")
async def get_confusion_matrix(request: Request):
    model_id = request.cookies.get('ppm-api').split(".")[0]
    path = f"data/results/{model_id}_matrix.svg"
    if not os.path.isfile(path):
        raise HTTPException(409, detail="Confusion matrix is not available")
    return FileResponse(path)


@router.get("/training-history")
async def get_training_history_image(request: Request):
    model_id = request.cookies.get('ppm-api').split(".")[0]
    path = f"data/results/{model_id}_history.svg"
    if not os.path.isfile(path):
        raise HTTPException(409, detail="Training history is not available")
    return FileResponse(path)


@router.get("/classification-report")
async def get_classification_report(request: Request):
    model_id = request.cookies.get('ppm-api').split(".")[0]
    path = f"data/results/{model_id}_report.json"
    if not os.path.isfile(path):
        raise HTTPException(409, detail="Report history is not available")
    return FileResponse(path)
