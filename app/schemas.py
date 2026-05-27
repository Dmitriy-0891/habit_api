from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Схема для создания привычки(то, что присылает клиент)
class HabitCreate(BaseModel):
    name: str
    
    
#Схема для ответа API(то, что получает клиент)
class HabitResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    quote: Optional[str] = None
    
    class Config:
        from_attributes = True #позволяет работать с ORM-объектами