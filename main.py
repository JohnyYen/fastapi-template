from fastapi import FastAPI
from src.api.v1.routers import api_router
from src.core.config import settings
from src.db.base import Base
from src.db.session import engine

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Una API moderna y asíncrona para gestionar usuarios, construida con FastAPI y SQLAlchemy.",
    version="1.0.0",
    contact={
        "name": "Tu Nombre",
        "url": "http://tuwebsite.com",
        "email": "tu@email.com",
    },
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operaciones para crear, leer, actualizar y eliminar usuarios.",
        }
    ]
)

@app.on_event("startup")
async def on_startup():
    await create_tables()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
