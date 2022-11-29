from typing import Union
from fastapi import Request, FastAPI

# uvicorn main:app --reload
# source env/bin/activate

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/")
async def log(request: Request):
    param = await request.json()
    print(param)
    return {"item_id": "success"}