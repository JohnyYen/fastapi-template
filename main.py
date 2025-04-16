from fastapi import FastAPI
from .src.api.v1.routers import api_router
from .src.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}