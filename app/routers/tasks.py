from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.TaskResponse], status_code=status.HTTP_200_OK)
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    is_completed: Optional[bool] = Query(None),
    sort: Optional[str] = Query("created_at", regex="^(id|title|created_at|is_completed)$"),
    order: Optional[str] = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None)
):
    tasks = crud.get_tasks(db, skip=skip, limit=limit, is_completed=is_completed, sort=sort, order=order, search=search)
    return tasks

@router.post("/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@router.get("/{task_id}", response_model=schemas.TaskResponse, status_code=status.HTTP_200_OK)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{task_id}", response_model=schemas.TaskResponse, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id, task_update)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return None