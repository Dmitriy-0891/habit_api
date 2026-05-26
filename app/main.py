from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.database import SessionLocal, engine, get_db

# Создаем таблицы в БД (при первом запуске)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Habit Tracker API",
    description = "API для трекера привычек с мотивирующими цитатами",
    version = "1.0.0"
)


#==========ЭНДПОИНТЫ==========

@app.post("/habits/", response_model=schemas.HabitResponse,
          status_code=status.HTTP_201_CREATED)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db)):
    """ 
    Создать новую привычку.
    Автоматически добавляет мотивирующую цитату из внешнего API.
    """
    return crud.create_habit(db=db, habit=habit)


@app.get("/habits/", response_model=List[schemas.HabitResponse])
def read_habits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список всех привычек.
    Поддерживает пагинацию: ?skip=0&limit=10
    """
    habits = crud.get_habits(db, skip=skip, limit=limit)
    return habits

@app.delete("/habits/{habit_id}", response_model = schemas.HabitResponse)
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    """
    Удалить привычку по ID.
    """
    db_habit = crud.delete_habit(db, habit_id=habit_id)
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Привычка не найдена")
    return db_habit

@app.get("/")
def root():
    return {"massage": "Добро пожаловать в Habit Tracker API!", "docs": "/docs"}

#============ Опционально: статистика ===========


@app.get("/stats/today/")
def today_stats(db: Session = Depends(get_db)):
    """ Показывает привычки, добавленные сегодня (как в CLI-версии)"""
    from datetime import datetime, datetime
    today_start = datetime.combine(date.today(), datetime.min.time())
    habits = db.query(models.Habit).filter(
        models.Habit.created_at >= today_start
    ).all()
    return {
        "date": str(date.today()),
        "count": len(habits),
        "habits": [h.name for h in habits]
    }