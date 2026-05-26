from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database import Base
from datetime import datetime

class Habit(Base):
    __tablename__ = "habits"
    
    id = Column(Integer, primery_key=True, Index=True)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    quote = Column(Text, nullable=True) #Мотивирующая цитата
    
    def __repr__(self):
        return f'<Habit(id={self.id}, name={self.name})>'