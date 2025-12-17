from datetime import date
from typing import List
from pydantic import BaseModel, field_validator


class Habit:
    def __init__(self, id: int, name: str, marks: List[date] = None):
        self.id = id
        self.name = name
        self.marks = marks if marks is not None else []
        self.streak = 0


class HabitBase(BaseModel):
    id: int
    name: str


class HabitUpdate(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Habit name cannot be empty')
        return v.strip()


class HabitResponse(HabitBase):
    marks: List[date]
    streak: int


class HabitCreate(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Habit name cannot be empty')
        return v.strip()


class HabitMarkResponse(BaseModel):
    id: int
    name: str
    last_marked_at: date
    streak: int


class HabitStatsResponse(BaseModel):
    id: int
    name: str
    total_marks: int
    current_streak: int
    max_streak: int
    success_rate: float
    last_dates: List[date]

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }