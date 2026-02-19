from fastapi import FastAPI ,APIRouter, Depends, UploadFile, Request
from helper.config import get_settings ,Setting
from controllers import DataController, ProjectController, ProcessController
from routes.schemes.data import ProcessRequest
from fastapi.responses import JSONResponse
import aiofiles
from models import ResponseStatus
import logging
from  models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk
loggrer = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data", 
    tags=["data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(request:Request,project_id:str, file: UploadFile, settings: Setting = Depends(get_settings)):

    project_model = ProjectModel(db_client=  request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

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
            "file_id": file_path.split("/")[-1],
        }

    )



@data_router.post("/process/{project_id}")
async def process_endpoint(request:Request,project_id:str,process_request: ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_rest = process_request.do_reset

    project_model = ProjectModel(db_client=  request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)


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
    file_chunks_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order= i +1,
            chunk_project_id=project.id
        )
        for i, chunk in enumerate(file_chunks)
        ]
    
    chunk_model = ChunkModel(db_client= request.app.db_client)

    if do_rest == 1:
        _ = await chunk_model.delete_chunks_by_project_id(
            project_id = project.id
        )
    no_records = await chunk_model.insert_many_chunks(chunks=file_chunks_records)

    return JSONResponse(
        content={
            "signal": ResponseStatus.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records
        }
    )
