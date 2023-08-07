import json
import os
import pickle
from os import listdir, curdir
from os.path import isfile, join

import numpy as np
import pandas as pd
from fastapi import HTTPException
from fastapi import APIRouter, Request
from fastapi import File, UploadFile
import pm4py
from keras.models import load_model
from keras.src.utils import pad_sequences

from evaluate_dataset.complexity import generate_pm4py_log
from helper.process_uploads import process_xes, process_csv
from train_model.utils import WINDOW_SIZE

router = APIRouter()


@router.post("")
def predict_next_event(request: Request, file: UploadFile = File(...)):
    session_id = request.cookies.get('ppm-api')
    model_id = session_id.split(".")[0]
    models = [f for f in listdir("data/models/") if isfile(join("data/models/", f)) and (model_id in f)]
    if len(models) == 0:
        raise HTTPException(status_code=404, detail="No model could not be found. Please train one first!")

    # write in new file
    if file.filename[-3:] == 'csv':
        process_csv(file, session_id, "info", "predictions")
    if file.filename[-3:] == 'xes':
        await process_xes(file, session_id, "predictions")

    # read ongoing process
    log_path = join(curdir, "data", "predictions", file.filename)
    log = pd.read_csv(log_path) if log_path.split(".")[-1] == "csv" else pm4py.read_xes(log_path)

    # read configs
    configs = {}
    config_path = os.path.join(os.curdir, f"data/configs/{model_id}.json")
    with open(config_path) as f:
        configs = json.load(f)

    # read encodings
    encodings = {}
    config_path = os.path.join(os.curdir, f"data/encodings/{model_id}.json")
    with open(config_path) as f:
        encodings = json.load(f)

    # read label encodings
    encodings_label = {}
    config_path = os.path.join(os.curdir, f"data/encodings/{model_id}_label.json")
    with open(config_path) as f:
        encodings_label = json.load(f)

    X = log["case:name"] if "case:name" in log else log[0]

    # encode event
    if configs.event_enc is not "FREQBASED":
        X_enc = [encodings[event] for event in X]
        max_length = configs["max_length"] if configs.sequ_enc == "PREPAD" else WINDOW_SIZE
        X_enc = pad_sequences(X_enc, value=0.0, dtype=object, maxlen=max_length)
    else:
        X_np = np.array(X)
        X_unique, counts = np.unique(X_np, return_counts=True)
        combined_X_count = zip(X_unique, counts)
        X_enc = [ combined_X_count[key] if key in combined_X_count else 0 for key in encodings]

    if configs.type == "DT" and (models) == 1 and '.sav' in models[0]:
        # D-Tree
        model = pickle.load(open(models[0], 'rb'))
        y_pred = model.predict(X_enc)
        y_pred = np.argmax(y_pred, axis=1)
        return {"next_event": y_pred, "process": X_enc}
    else:
        model_accuracies = [model_names.split("_")[-1].rsplit(".", 1)[0] for model_names in models]
        max_accuracy = max(list(model_accuracies), default=0)
        model_path = f"data/models/{model_id}_{str(max_accuracy)}.keras"

        if not isfile(model_path):
            raise HTTPException(status_code=404, detail="No model could not be found. Please train one first!")

        model = load_model(model_path)
        y_pred = model.predict(X_enc, verbose=0)
        y_pred = np.argmax(y_pred, axis=1)
        return {"next_event": y_pred, "process": X_enc}
