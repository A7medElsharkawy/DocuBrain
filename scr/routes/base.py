from fastapi import FastAPI ,APIRouter
import os

base_router = APIRouter(
    prefix="/api/v1",
    tags=["base"]
)


@base_router.get("/welcome")
async def welcome_message():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    return f"Welcome to {app_name} version {app_version}!"