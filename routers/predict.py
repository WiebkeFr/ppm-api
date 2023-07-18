import pickle
from os import listdir, curdir
from os.path import isfile, join

import pandas as pd
from fastapi import HTTPException
from fastapi import APIRouter, Request
from fastapi import File, UploadFile
import pm4py

from evaluate_dataset.complexity import generate_pm4py_log

router = APIRouter()


@router.post("")
def predict_next_event(request: Request, file: UploadFile = File(...)):
    session_id = request.cookies.get('ppm-api')
    model_id = session_id.split(".")[0]
    models = [f for f in listdir("data/models/") if isfile(join("data/models/", f)) and (model_id in f)]
    if len(models) == 0:
        raise HTTPException(status_code=404, detail="No model could not be found. Please train one first!")

    # write in new file
    contents = await file.read()
    file_content = contents.decode('UTF-8')
    path = join(curdir, "data", "predictions", "{}.xes".format(model_id))
    with open(path, "w+") as file:
        file.write(file_content)
        file.close()

    print(path)

    # read ongoing process
    log_path = join(curdir, "data", "logs", path)
    log = pd.read_csv(log_path) if path.split(".")[-1] == "csv" else pm4py.read_xes(log_path)
    print(log)
    pm4py_log = generate_pm4py_log(log_path)
    print(pm4py_log)
    # "lifecycle:transition"

    if len(models) == 1 and '.sav' in models[0]:
        # D-Tree
        model = pickle.load(open(models[0], 'rb'))
        y_pred = model.predict(self.X_test)
        return {"next_event": y_pred}

    else:
        model_accuracies = [model_names.split("_")[-1].rsplit(".", 1)[0] for model_names in models]
        max_accuracy = max(list(model_accuracies), default=0)
        model_path = f"data/models/{model_id}_{str(max_accuracy)}.keras"

        if not isfile(model_path):
            raise HTTPException(status_code=404, detail="No model could not be found. Please train one first!")

    print("hier")
    return {"hier": "hie"}
