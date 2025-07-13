from fastapi import FastAPI
from routes.data import data_router

from routes.base import base_router

app = FastAPI()
# Include the base router for general API endpoints
app.include_router(base_router)

app.include_router(data_router)