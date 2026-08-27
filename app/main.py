from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder

from app.routers import tasks
from app.database import Base, engine
from app.models import Task
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="Simple CRUD API for managing tasks",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": jsonable_encoder(exc.errors())
        },
    )