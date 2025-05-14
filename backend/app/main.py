from typing import Union
from fastapi import FastAPI
from app.api.upload import router

app = FastAPI()

app.include_router(router, prefix="/api")

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# backend/app/api/upload.py


