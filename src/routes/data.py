from fastapi import FastAPI ,APIRouter, Depends, UploadFile
from helper.config import get_settings ,Setting
from controllers import DataController
from fastapi.responses import JSONResponse
from controllers import ProjectController
import os
import aiofiles
from models import ResponseStatus
import logging

loggrer = logging.getLogger('uvicorn.error')
data_router = APIRouter(
    prefix="/api/v1/data", 
    tags=["data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str, file: UploadFile, settings: Setting = Depends(get_settings)):
    app_name = settings.APP_NAME
    app_version = settings.APP_VERSION
    data_controller = DataController()
    is_valid,signal = data_controller.validate_uploaded_file(file)
    if not is_valid:
        return JSONResponse(status_code=400, content={"error": signal})
    
    project_dir_path =  ProjectController().get_project_path(project_id)
    file_path = data_controller.generate_unique_filename(file.filename, project_id)
    
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        loggrer.error(f"Error uploading file: {str(e)}")
        return JSONResponse(status_code=400, 
                            content={"signal": ResponseStatus.FILE_UPLOAD_FAILED.value})

    return JSONResponse(
        content={
            "signal": ResponseStatus.UPLOAD_SUCCESS.value,
        }

    )




