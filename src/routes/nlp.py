from fastapi import FastAPI,APIRouter,status,Request
from .schemes.nlp import PushRequest,SearchRequest
from models.ProjectModel import ProjectModel
from controllers import NLPController
from fastapi.responses import JSONResponse 
from models import ResponseSignal
from models.ChunkModel import ChunkModel
import os 
import logging

logger=logging.getLogger("uvicorn.error")


nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1","nlp"],
)

@nlp_router.post("/index/push/{prject_id}") 
async def index_project(request :Request, prject_id: str,push_request: PushRequest):

    project_model=await ProjectModel.create_instance(
        db_client=request.app.db_client
        )
    
    chunk_model= await ChunkModel.create_instance(
            db_client=request.app.db_client
            )
    
    
    project = await project_model.get_or_create_one(project_id=prject_id)


    if not project:
        return JSONResponse(
            content={"Signal": ResponseSignal.PROJECT_NOT_FOUND.value},
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    nlp_controller=NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
    )



    has_record=True
    page_no=1
    inserted_item=0
    idx=0

    while has_record :

        page_chunks= await chunk_model.get_project_chunks(project_id=project.id,
                                                    page_no=page_no)
        
        if len(page_chunks):
            page_no+=1
            

        if not page_chunks or  len(page_chunks)==0 :
            has_record=False
            break

        chunks_ids=list(range(idx,idx+len(page_chunks)))

        idx+=len(page_chunks)

        is_inserted= nlp_controller.index_into_vectordb(
            project=project, 
            chunks=page_chunks,
            chunks_id=chunks_ids,
            do_reset=push_request.do_reset

        )

        if not is_inserted :
            return JSONResponse(
            content={"Signal": ResponseSignal.CHUNKS_NOT_INSERTED.value},
            status_code=status.HTTP_400_BAD_REQUEST
            )
        inserted_item+=len(page_chunks)
    
    return JSONResponse(
            content={"Signal": ResponseSignal.CHUNKS_INSERTED.value,
            "message":f"Total {inserted_item} Chunks inserted"},
            status_code=status.HTTP_200_OK
            )

@nlp_router.get("/index/info/{prject_id}") 
async def index_info(request :Request, prject_id: str):

    project_model=await ProjectModel.create_instance(
        db_client=request.app.db_client
        )
    
    project = await project_model.get_or_create_one(project_id=prject_id)

    nlp_controller=NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
    )


    if not project:
        return JSONResponse(
            content={"Signal": ResponseSignal.PROJECT_NOT_FOUND.value},
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    project_collection_info= nlp_controller.get_vectordb_collection_info(
        project=project
                     )
    
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"Signal": ResponseSignal.COLLECTION_INFO_RETRIEVED.value,
                     "content":project_collection_info},
        
            
        )

@nlp_router.post("/index/search/{prject_id}") 
async def index_info(request :Request, prject_id: str,search_request: SearchRequest):


    project_model=await ProjectModel.create_instance(
        db_client=request.app.db_client
        )
    
    project = await project_model.get_or_create_one(project_id=prject_id)

    nlp_controller=NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
    )


    if not project:
        return JSONResponse(
            content={"Signal": ResponseSignal.PROJECT_NOT_FOUND.value},
            status_code=status.HTTP_404_NOT_FOUND
        )
    result_search=nlp_controller.search_in_vectordb(
        project=project,
        text=search_request.text,
        limit=search_request.limit
    )

    return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content={

                "content":[reslut.dict( ) for reslut in result_search]
                
               
                })


