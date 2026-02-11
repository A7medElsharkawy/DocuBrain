from fastapi import FastAPI
from pydantic import BaseModel
from helper.config import Setting
from routes import base


app = FastAPI()
app.include_router(base.base_router)