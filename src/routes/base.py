from fastapi import FastAPI,APIRouter,Depends
import os  

from helpers.config import get_settings, Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get("/")
async def welcome_message(app_settings: Settings = Depends(get_settings)):
    
    # Load environment variables
    app_name= app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    OpenAI_API_KEY = app_settings.OpenAI_API_KEY
    return {"message": "Welcome to the FastAPI application!",
            "app_name": app_name,
            "app_version": app_version  ,
            "OpenAI_API_KEY": OpenAI_API_KEY}