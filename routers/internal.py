import itertools
import typing

from fastapi import APIRouter
from starlette.requests import Request

from routers.train import Model_Info, start_training

router = APIRouter()


@router.get("/train")
def train_all_models(request: Request):
    file_name = request.cookies.get('ppm-api')
    types = typing.get_args(Model_Info.model_fields["type"].annotation)
    sequ_encs = typing.get_args(Model_Info.model_fields["sequ_enc"].annotation)
    event_encs = typing.get_args(Model_Info.model_fields["event_enc"].annotation)

    all_results = {}
    for t, s, e in list(itertools.product(types, sequ_encs, event_encs)):
        model_info = Model_Info(type = t, sequ_enc= s, event_enc= e)
        print(model_info)
        training_result = start_training(file_name, model_info, True)
        all_results[f"{t}_{s}_{e}"] = training_result
        print(training_result)

    print(all_results)
    return all_results
