from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app import models, schemas


def get_tasks(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        is_completed: bool = None,
        sort: str = "created_at",
        order: str = "desc",
        search: str = None
):
    query = db.query(models.Task)

    if search is not None:
        query = query.filter(models.Task.title.ilike(f"%{search}%"))

    if is_completed is not None:
        query = query.filter(models.Task.is_completed == is_completed)

    if sort in ["id", "title", "created_at", "is_completed"]:
        column = getattr(models.Task, sort)
        if order == "asc":
            query = query.order_by(asc(column))
        else:
            query = query.order_by(desc(column))

    return query.offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None

    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if not db_task:
        return None

    db.delete(db_task)
    db.commit()
    return db_task