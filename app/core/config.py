import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TaskPulse REST API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "bhanu_devops_secret_key_super_secure_2026_change_in_prod")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # SQLite default, seamlessly replaceable with postgresql://user:pass@host/db
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./taskpulse.db")

    class Config:
        case_sensitive = True

settings = Settings()
