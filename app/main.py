from fastapi import FastAPI, status
from app.routers import tasks
from app.database import Base, engine
from app.models import Task

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="Simple CRUD API for managing tasks",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}