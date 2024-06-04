from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sys_database_url:str
    database_url:str
    
    class Config:
        env_file = ".env"

settings = Settings()

