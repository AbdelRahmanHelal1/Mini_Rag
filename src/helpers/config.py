from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str 
    APP_VERSION: str 
    OpenAI_API_KEY: str
    FILE_ALLOWED_EXTENSIONS: list
    FILE_MAX_SIZE: int = 10485760            # 10 MB
    FILE_CHUNK_SIZE: int 
    MONOGO_DB_URL : str
    MONGO_DB_NAME : str

    GENERATION_BACKEND :str
    EMBEDDING_BACKEND :str

    OpenAI_API_KEY :str =None
    COHERE_API_KEY :str =None

    GENERATION_MODEL_ID :str =None
    EMBEDDING_MODEL_ID :str =None
    EMBEDDING_MODEL_ID_SIZE :int =None

    DEFAULT_MAX_INPUT_CHARACTER :int =None
    DEFAULT_MAX_OUTPUT_CHARACTER:int =None
    GENERATION_DAFAULT_TEMPERATURE :float =None

    VECTOR_DB_PROVIDER :str 
    VECTOR_DB_PATH :str  
    VECTOR_DB_DISTANCE_METRIC :str =None

    PRIMARY_LANGUAGE: str="arb"
    DEFULT_LANGUAGE:  str="arb"
    
    class Config:
        env_file = ".env"
       

def get_settings() : 
    return Settings()