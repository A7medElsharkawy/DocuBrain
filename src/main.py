from fastapi import FastAPI
from pydantic import BaseModel
from helper.config import Setting
from routes import base
from routes import data


app = FastAPI()
app.include_router(base.base_router)
app.include_router(data.data_router)