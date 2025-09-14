from fastapi import FastAPI
from routes.data import data_router
from routes.base import base_router
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONOGO_DB_URL)
    app.db_client = app.mongo_conn[settings.MONGO_DB_NAME]
    print("Connected to MongoDB!")

@app.on_event("shutdown")
async def shutdown_event():
    app.mongo_conn.close()
    print("Disconnected from MongoDB!")


# Include the base router for general API endpoints
app.include_router(base_router)

app.include_router(data_router)