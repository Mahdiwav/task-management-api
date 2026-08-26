from fastapi import FastAPI, status

app = FastAPI(
    title="Task Management API",
    description="Simple CRUD API for managing tasks",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}