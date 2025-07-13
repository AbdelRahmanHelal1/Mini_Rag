from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str 
    APP_VERSION: str 
    OpenAI_API_KEY: str
    FILE_ALLOWED_EXTENSIONS: list
    FILE_MAX_SIZE: int = 10485760            # 10 MB
    FILE_CHUNK_SIZE: int 
    
    class Config:
        env_file = ".env"
       

def get_settings() : 
    return Settings()