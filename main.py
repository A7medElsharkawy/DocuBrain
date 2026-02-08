from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
import os

app = FastAPI()

@app.get("/welcome")
def welcome_message():
    app_name = os.getenv("APP_NAME", "DocuBrain")
    app_version = os.getenv("APP_VERSION", "0.1.0")
    return f"Welcome to {app_name} version {app_version}!"