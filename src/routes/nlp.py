from fastapi import APIRouter,Request,status,Request
import logging 
from fastapi.responses import JSONResponse
from openai.types import embedding
from controllers import NlpController
from routes.schemes.nlp import PushRequest
from models.ProjectModel import ProjectModel
from models.enums import ResponseEnums
from models import ChunkModel
logger = logging.getLogger('uvicorn.error')

nlp_router = APIRouter(
    prefix='/api/v1/nlp',
    tags=['nlp_v1, "nlp'],

)
@nlp_router.post("/index/push/{project_id}")
async def index_project(request : Request, project_id : str,push_request: PushRequest):
    
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    
    chunk_model =  await ChunkModel.create_instance(
        db_client=request.app.db_client
    )

    project = project_model.get_project_or_create_one(project_id=project_id)
    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseEnums.ResponseStatus.PROJECT_NOT_FOUND_ERROR.value
            } 
        )
    
    nlp_controller = NlpController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        emebedding_client=request.app.emebedding_client
    )
    has_records = True
    page_no =1
    inserted_items_count = 0
    while has_records:
        page_chunks = chunk_model.get_project_chunks(project_id=project_id,page_no=page_no)

        if len(page_chunks):
            page_no += 1
        if not page_chunks or len(page_chunks) == 0:
            has_records = False
            break
        
        is_inserted = nlp_controller.index_info_vector_db(
            project=project,
            chunks=page_chunks,
            do_reset=push_request
        )
    
        if not is_inserted:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal":ResponseEnums.ResponseStatus.INSERT_INTO_VECTOREDB_ERROR.value
                }
            )
        inserted_items_count += len(page_chunks)

    return JSONResponse(
        content={
            "signal": "inserted_ secusse",
            "inserted_items_count": inserted_items_count
        }
    )



    