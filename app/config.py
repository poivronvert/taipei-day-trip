from pydantic_settings import BaseSettings
import os
from pathlib import Path
from dotenv import load_dotenv

# 嘗試載入 .env 文件
env_path = Path("../.env")
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    sys_database_url:str = os.getenv("SYS_DATABASE_URL")
    database_url:str = os.getenv("DATABASE_URL")
    secret_key:str = os.getenv("SECRET_KEY")

settings = Settings()

