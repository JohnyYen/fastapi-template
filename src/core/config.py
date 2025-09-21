from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI Project"
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()