from fastapi import FastAPI,APIRouter,Depends,UploadFile,status,Request
import os 
from fastapi.responses import JSONResponse 
from fastapi import File
# from controllers.DataController import DataController
from models import ResponseSignal
from helpers.config import get_settings, Settings
from controllers import ProjectController,DataController,ProcessController
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.db_schemes import Data_Chunk
from models.ChunkModel import ChunkModel
import aiofile
import logging

logger=logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_router.post("/upload/{prject_id}")
async def upload_file(request :Request, prject_id: str,file: UploadFile= File(...),
                      app_settings: Settings = Depends(get_settings)):
    
    project_model=ProjectModel(
        db_client=request.app.db_client
        )
    
    project = await project_model.get_or_create_one(project_id=prject_id)


    """
    Endpoint to upload a file.
    """
    data_controller = DataController(app_settings)
    is_valid,result_signal = data_controller.validate_uploaded_file(file)

    if is_valid:
        file_path,file_id =data_controller.generate_Uniqe_file_path(project_id=prject_id, file_name=file.filename)
        print(f"File will be saved to: {file_path}")
        
        try:
            
            async with aiofile.AIOFile(file_path, 'wb') as f:
                while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                    await f.write(chunk)
        except Exception as e:
            
            logger.error(f"Error Uploading file :{e}")
            return JSONResponse(
                content={"Signal": ResponseSignal.FILE_UPLOAD_FAILED.value, "Error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

    return JSONResponse(
            content={"Signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id":file_id ,
            "prject_id" : str(project.id)
            }
            
            )

    
@data_router.post("/process/{prject_id}") 
async def process_file(request :Request,prject_id:str, processrequest: ProcessRequest)  :

    file_id= processrequest.file_id
    chunk_size= processrequest.chunk_size
    overlap= processrequest.overlap
    do_reset=processrequest.do_reset

    project_model=ProjectModel(
        db_client=request.app.db_client
        )
    
    
    
    project = await project_model.get_or_create_one(project_id=prject_id)




    process_controller=ProcessController(prject_id,file_id)

    file_content= process_controller.get_file_content()

    file_chunks= process_controller.Process_file_content(
        content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,          
        overlap=overlap
    )

    if file_chunks is None or len(file_chunks)==0:
        return JSONResponse(
            content={"Signal": ResponseSignal.FILE_PROCESSING_FAILED.value,
            "Error":"No chunks were created from the file."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )  

    file_chunks_records=[

            Data_Chunk(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i+1,
                chunk_project_id=project.id
            )

        for i,chunk in enumerate( file_chunks)
    ]

    chunk_model=ChunkModel(
        db_client=request.app.db_client
        )
    
    if do_reset == 1 :   
        _= await chunk_model.delete_chunks_by_project_id(
            project_id=project.id
        )

    
    
    no_records= await chunk_model.insert_many_chunks(
        chunks=file_chunks_records
    )

    return JSONResponse(
            content={"Signal": ResponseSignal.FILE_PROCESSING_SUCCESS.value,    
            
            "no_of_chunks":no_records
            }
    )
        

    
      