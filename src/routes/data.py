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
from models.AssetModel import AssetModel
import aiofile
import logging
from bson import ObjectId
from models.db_schemes import Asset
from models.enums.AssetTypeEnums import AssetTypeEnums

logger=logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_router.post("/upload/{prject_id}")
async def upload_file(request :Request, prject_id: str,file: UploadFile= File(...),
                      app_settings: Settings = Depends(get_settings)):

    
    
    project_model=await ProjectModel.create_instance(
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
    asset_model= await AssetModel.create_instance(
        db_client=request.app.db_client
        )   
    

    asset_resource=Asset(
    asset_project_id=ObjectId(project.id),
    asset_type=AssetTypeEnums.File.value,
    asset_name=file_id,
    asset_size=os.path.getsize(file_path),




    )
    asset_record = await asset_model.create_asset(asset=asset_resource)
        

    return JSONResponse(
            content={"Signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id":str(asset_record.id) ,
            "file_name:":file_id,
            "prject_id" : str(project.id)
            }
            
            )

    
@data_router.post("/process/{prject_id}") 
async def process_file(request :Request,prject_id:str, processrequest: ProcessRequest)  :

    #file_id= processrequest.file_id
    chunk_size= processrequest.chunk_size
    overlap= processrequest.overlap
    do_reset=processrequest.do_reset

    project_model=await ProjectModel.create_instance(
        db_client=request.app.db_client
        )
    print(prject_id,"##"*50)
  
    project = await project_model.get_or_create_one(project_id=prject_id)

    asset_model= await AssetModel.create_instance(
        db_client=request.app.db_client
        ) 

    

    if processrequest.file_id :
        #project_files_ids=[processrequest.file_id]
        asset_record= await asset_model.get_asset_record(
            asset_project_id=project.id,
            asset_name=processrequest.file_id
        )
        if asset_record is None :
            return JSONResponse(
                content={"Signal": ResponseSignal.FILE_PROCESSING_FAILED.value,
                "Error":"The specified file_id does not exist in the project."},
                status_code=status.HTTP_404_NOT_FOUND
            )

        project_files_ids={
            asset_record.id:asset_record.asset_name

        }




    else :
        project_files= await asset_model.get_all_project_assets(
            asset_project_id=project.id,
            asset_type=AssetTypeEnums.File.value
        )
        

        project_files_ids={

           rec.id:rec.asset_name
            for rec in project_files 
        }
    
    if len(project_files_ids)==0 :
        return JSONResponse(
            content={"Signal": ResponseSignal.NO_FILES_TO_PROCESS.value,
            "Error":"No files found for processing in the project."},
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    process_controller=ProcessController(prject_id)
        
    no_records=0
    no_files=0

    chunk_model= await ChunkModel.create_instance(
            db_client=request.app.db_client
            )

    if do_reset == 1 :   
            _= await chunk_model.delete_chunks_by_project_id(
                project_id=project.id
            )

    for asset_id,file_id in project_files_ids.items():
       

        file_content= process_controller.get_file_content(file_id)

        if file_content is None :
            logger.error(f"Error Processing file {file_id} : Unsupported file type or file path not exist.")
            continue




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
                    chunk_project_id=project.id,
                    chunk_asset_id=asset_id
                )
            

            for i,chunk in enumerate( file_chunks)
        ]

        

        no_records += await chunk_model.insert_many_chunks(
            chunks=file_chunks_records
        )

        no_files +=1

    return JSONResponse(
            content={"Signal": ResponseSignal.FILE_PROCESSING_SUCCESS.value,    
            
            "no_of_chunks":no_records,
            "Processed_files":no_files
            }
    )
        

    
      
