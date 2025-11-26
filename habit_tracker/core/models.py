from datetime import date
from typing import List
from pydantic import BaseModel, field_validator


class Habit:
    """Внутренняя модель привычки для хранения в памяти."""
    def __init__(self, id: int, name: str, marks: List[date] = None):
        self.id = id
        self.name = name
        self.marks = marks if marks is not None else []
        self.streak = 0

class HabitBase(BaseModel):
    """Базовая модель для ответов API."""
    id: int
    name: str

class HabitUpdate(BaseModel):
    """Модель для обновления привычки."""
    name: str

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Habit name cannot be empty')
        return v.strip()
    
class HabitResponse(HabitBase):
    """Полная информация о привычке."""
    marks: List[date]
    streak: int

class HabitCreate(BaseModel):
    """Модель для создания привычки."""
    name: str
    
    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        # TODO: Реализовать проверку на пустое имя
        if not v.strip():
            raise ValueError('Habit name cannot be empty')
        return v.strip()

# TODO: Реализовать остальные модели (HabitMarkResponse, HabitListResponse)

class HabitMarkResponse(BaseModel):
    id: int
    name: str
    last_marked_at: str
    streak: int

HabitListResponse = HabitResponse