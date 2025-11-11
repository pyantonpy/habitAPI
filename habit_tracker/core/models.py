from datetime import date
from typing import List
from pydantic import BaseModel, field_validator


class Habit:
    """Внутренняя модель привычки для хранения в памяти."""
    
    def __init__(self, id: int, name: str):
        # TODO: Инициализировать поля
        self.id = id
        self.name = name
        self.marks =  list()

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

class HabitResponse(BaseModel):
    """Модель ответа после создания привычки."""
    # TODO: Добавить поля id и name
    id: int
    name: str

# TODO: Реализовать остальные модели (HabitMarkResponse, HabitListResponse)

class HabitMarkResponse(BaseModel):
    id: int
    name: str
    last_marked_at: str

class HabitListResponse(BaseModel):
    id: int
    name: str
    marks: List[str]