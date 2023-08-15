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

from utils.process_uploads import process_xes

router = APIRouter()


@router.post("")
async def predict_next_event(request: Request, file: UploadFile = File(...)):
    print(file.filename)
    session_id = request.cookies.get('ppm-api')
    model_id = session_id.split(".")[0]
    models = [f for f in listdir("data/models/") if isfile(join("data/models/", f)) and (model_id in f)]
    if len(models) == 0:
        raise HTTPException(status_code=404, detail="No model could not be found. Please train one first!")

    # get unfinished sequence
    X = []
    if file.filename[-3:] == 'csv':
        X = pd.read_csv(file.file).iloc[:, 1]
        X = list(X.astype(str))
    if file.filename[-3:] == 'xes':
        await process_xes(file, model_id, "predictions")
        log_path = join(curdir, "data", "predictions", f"{model_id}.xes")
        X = list(pm4py.read_xes(log_path)["concept:name"])

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
        reversed_encoding_labels = json.load(f)
        encodings_label = {v: k for k, v in reversed_encoding_labels.items()}

    # encode the trace
    if configs["event_enc"] != "FREQBASED":
        X_enc = [encodings[event] for event in X]
        max_length = configs["max_length"]
        if len(X_enc) < max_length:
            X_shape = np.array(X_enc).shape
            empty_array = np.zeros(shape=(max_length, X_shape[1]))
            empty_array[-X_shape[0]:] = X_enc
            X_enc = empty_array
        else:
            X_enc = X_enc[-max_length:]
        X_enc = np.asarray(X_enc).astype('float32')
    else:
        X_np = np.array(X)
        X_unique, counts = np.unique(X_np, return_counts=True)
        combined_X_count = zip(X_unique, counts)
        X_enc = [ combined_X_count[key] if key in combined_X_count else 0 for key in encodings]

    model_path = f"data/models/{models[0]}"
    if not isfile(model_path):
        raise HTTPException(status_code=404, detail="No model could not be found. Please train one first!")

    X_enc = np.array([X_enc])

    if configs["type"] == "DT" and len(models) == 1 and '.sav' in models[0]:
        # Decision Tree
        if len(X_enc.shape) != 2:
            samples, nx, ny = X_enc.shape
            X_enc = X_enc.reshape((samples, nx * ny))
        model = pickle.load(open(model_path, 'rb'))
        y_pred = model.predict(X_enc)
        y_pred = np.argmax(y_pred, axis=1)[0]
        y_label = encodings_label[str(y_pred)]
        print(X, y_label)
        return {"next_event": y_label, "process": X}
    else:
        # LSTM or CNN
        if len(X_enc.shape) != 3:
            X_enc = np.reshape(X_enc, (*X_enc.shape, 1))
        model = load_model(model_path)
        y_pred = model.predict(X_enc, verbose=0)
        y_pred = np.argmax(y_pred, axis=1)[0]
        y_label = encodings_label[str(y_pred)]
        print(X, y_label)
        return {"next_event": str(y_label), "process": X}
