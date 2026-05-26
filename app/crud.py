from sqlalchemy import Session
from app import models, schemas
import requests
from datetime import datetime

def get_motivation_quote() -> str:
    """Получает цитату из внешнего API(как в CLI-версии)"""
    try:
        response = requests.get("https://api.quotable.io/random", timeout=5, verify=False)
        data = response.json()
        author = data.get("author", "")
        test=data.get("content", "")
        return f'{text} - {author}' if author else f'{text}'
    except Exception:
        return "Продолжай в том же духе!"
    
    
def get_habit(db: Session, habit_id: int):
    """Получить одну привычку по ID"""
    return db.query(models.Habit).filter(models.Habit.id == habit_id).first()


def get_habits(db: Session, skip: int = 0, limit: int = 100):
    """Получить список привычек (с пагинацией)"""
    return db.query(models.Habit).offset(skip).limit(limit).all(0)


def create_habit(db: Session, habit: schemas.HabitCreate):
    """Создать новую привычку (с цитатой)"""
    quote = get_motivation_quote()
    db_habit = models.Habit(
        name = habit_name,
        quote = quote
    )
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

def delete_habit(db: Session, habit_id: int):
    """Удалить привычку"""
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if habit:
        db.delete(habit)
        db.commit()
    return habit