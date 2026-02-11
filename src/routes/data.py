from fastapi import FastAPI ,APIRouter, Depends, UploadFile
from helper.config import get_settings ,Setting

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str, file: UploadFile, settings: Setting = Depends(get_settings)):
    app_name = settings.APP_NAME
    app_version = settings.APP_VERSION
    return f"Welcome to {app_name} version {app_version}!"