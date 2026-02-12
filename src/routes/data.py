from fastapi import FastAPI ,APIRouter, Depends, UploadFile
from helper.config import get_settings ,Setting
from controllers import DataController, ProjectController, ProcessController
from routes.schemes.data import ProcessRequest
from fastapi.responses import JSONResponse
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

    data_controller = DataController()
    is_valid,signal = data_controller.validate_uploaded_file(file)
    if not is_valid:
        return JSONResponse(status_code=400, content={"error": signal})
    
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
            "file_id": file_path.split('/')[-1]
        }

    )



@data_router.post("/process/{project_id}")
async def process_endpoint(project_id:str,process_request: ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size

    process_controller = ProcessController(project_id = project_id)
    file_content = process_controller.get_file_content(file_id)
    file_chunks = process_controller.process_file_content(
        file_id=file_id, 
        file_content=file_content,
        chunk_size=chunk_size,
        chunk_overlap=overlap_size)
    
    if not file_chunks or len(file_chunks) == 0:
        return JSONResponse(
            status_code=400,
            content={"signal": ResponseStatus.PROCESSING_FAILED.value}
        )
    return file_chunks
