from __future__ import annotations

import json
import os

import pandas as pd
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

from train_model.cnn import CNN_Model
from train_model.dtree import DT_Model
from train_model.lstm import LSTM_Model
from train_model.model import PPMModel, EPOCH_SIZE
from train_model.utils import log_state
from typing import Literal, Union

router = APIRouter()


class Model_Info(BaseModel):
    type: Literal['LSTM', 'CNN', 'DT']
    sequ_enc: Literal['PREPAD', 'CONT']
    event_enc: Literal['ONEHOT', 'EMBEDDED', 'FREQBASED']


def start_training(file_name: str, model_info: Model_Info, additional_evaluation: bool):
    model = PPMModel("", "", "DEFAULT")

    if model_info.type == 'LSTM':
        model = LSTM_Model(model_info.sequ_enc, model_info.event_enc, file_name)
    elif model_info.type == 'CNN':
        model = CNN_Model(model_info.sequ_enc, model_info.event_enc, file_name)
    elif model_info.type == 'DT':
        model = DT_Model(model_info.sequ_enc, model_info.event_enc, file_name)

    model_id = file_name.split(".")[0]
    progress_path = f"data/training/{model_id}.txt"
    log_state(progress_path, "TRAIN")
    training_result = model.train(evaluate=additional_evaluation)
    if additional_evaluation:
        return training_result
    log_state(progress_path, "EVALUATE")
    model.evaluate_test_prediction()
    model.evaluate_history()
    log_state(progress_path, "DONE")


@router.post("")
async def train_model(request: Request, model_info: Model_Info, background_tasks: BackgroundTasks,
                      overwrite: Union[str, None] = None):
    print(model_info)
    id = request.cookies.get('ppm-api').split(".")[0]
    training_path = f"data/training/{id}.csv"

    config_path = os.path.join(os.curdir, f"data/configs/{id}.json")
    with open(config_path, "w+") as outfile:
        json.dump(model_info.model_dump(), outfile)

    if os.path.isfile(training_path) and overwrite != "true":
        return {"state": "warning-duplicate"}
    background_tasks.add_task(start_training, request.cookies.get('ppm-api'), model_info, False)
    return {"state": "success"}


@router.get("/training-progress")
async def get_training_progress(request: Request):
    session_id = request.cookies.get('ppm-api').split(".")[0]
    result_path = f"data/results/{session_id}.svg"

    try:
        state = False
        with open(f'data/training/{session_id}.txt', "r") as f:
            state = f.read()
            f.close()

        if state == "DONE":
            return JSONResponse({"state": "success", "progress": "1"})

        if state == "TRAIN":
            return JSONResponse({"state": "training", "progress": "0"})

        if state == "EVALUATE":
            return JSONResponse({"state": "evaluate", "progress": "1"})

        if "ERROR" in state:
            return JSONResponse({"state": "error", "progress": "-1"})

        if int(state) + 1 < EPOCH_SIZE:
            return JSONResponse({"state": "training", "progress": str((int(state) + 1) / EPOCH_SIZE)})

    except (TypeError, pd.errors.EmptyDataError, FileNotFoundError) as e:
        return JSONResponse({"state": "training", "progress": "0"})

    return JSONResponse({"state": "error", "progress": "-1"})
