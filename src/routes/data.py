from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
import os 
from fastapi.responses import JSONResponse 
from fastapi import File
# from controllers.DataController import DataController
from models import ResponseSignal
from helpers.config import get_settings, Settings
from controllers import ProjectController,DataController
import aiofile
import logging

logger=logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_router.post("/upload/{prject_id}")
async def upload_file(prject_id: str,file: UploadFile= File(...),
                      app_settings: Settings = Depends(get_settings)):
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
            "file_id":file_id})

    
            

    
      