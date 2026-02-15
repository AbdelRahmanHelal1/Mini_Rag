from fastapi import FastAPI
from routes.data import data_router
from routes.base import base_router
from routes.nlp import nlp_router 
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm import LLMProviderFactory
from stores.vectordb import VectorDBProviderFactory
from stores.llm.Templete.Tempelete_parser import TempleteParser
import logging
app = FastAPI()

logger = logging.getLogger(__name__)
async def startup_event():
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONOGO_DB_URL)
    app.db_client = app.mongo_conn[settings.MONGO_DB_NAME]
    logger.info("Connected to MongoDB!")

    # Generation
    llm_provider_factory=LLMProviderFactory(settings)
    app.generation_client=llm_provider_factory.create(settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(settings.GENERATION_MODEL_ID)

    # Embedding
    app.embedding_client=llm_provider_factory.create(settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(settings.EMBEDDING_MODEL_ID ,
                                             settings.EMBEDDING_MODEL_ID_SIZE)
    # Vector DB
    vectordb_provider_factory=VectorDBProviderFactory(settings)
    app.vectordb_client=vectordb_provider_factory.create(settings.VECTOR_DB_PROVIDER)
    
    app.vectordb_client.Connect()

    app.Tempelete_parser=TempleteParser(
        language=settings.PRIMARY_LANGUAGE,
        defult_language=settings.DEFULT_LANGUAGE
    )


async def shutdown_event():
    app.mongo_conn.close()
    print("Disconnected from MongoDB!")

    app.vectordb_client.Disconnect()
    print("Disconnected from VectorDB!")


# app.router.lifespan.on_startup.append(startup_event)
# app.router.lifespan.on_shutdown.append(shutdown_event)

app.on_event("startup")(startup_event)
app.on_event("shutdown")(shutdown_event)

# Include the base,data,nlp router for general API endpoints
app.include_router(base_router)
app.include_router(data_router)
app.include_router(nlp_router)