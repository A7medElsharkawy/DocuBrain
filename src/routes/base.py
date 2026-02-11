from fastapi import FastAPI ,APIRouter, Depends
from helper.config import get_settings ,Setting


base_router = APIRouter(
    prefix="/api/v1",
    tags=["base"]
)

    
@base_router.get("/welcome")
async def welcome_message(settings: Setting= Depends(get_settings)):
    app_name = settings.APP_NAME
    app_version = settings.APP_VERSION
    return f"Welcome to {app_name} version {app_version}!"