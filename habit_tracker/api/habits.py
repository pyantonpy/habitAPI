from typing import List
from fastapi import APIRouter, status
from habit_tracker.core import services
from habit_tracker.core.models import (
    HabitCreate, 
    HabitResponse, 
    HabitMarkResponse,
    HabitListResponse
)

router = APIRouter()


@router.post("/habits/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(habit: HabitCreate):
    """Создать новую привычку."""
    # TODO: 1. Вызвать services.create_habit() с habit.name
    # TODO: 2. Вернуть HabitResponse с id и name созданной привычки

    new_habit = services.create_habit(habit.name)
    new_habit_res = HabitResponse(id=new_habit.id, name=new_habit.name)

    return new_habit_res


@router.post("/habits/{habit_id}/mark/", response_model=HabitMarkResponse)
def mark_habit(habit_id: int):
    """Отметить выполнение привычки за текущий день."""
    # TODO: 1. Вызвать services.mark_habit() с habit_id
    # TODO: 2. Получить последнюю дату из habit.marks
    # TODO: 3. Отформатировать дату в строку (YYYY-MM-DD)
    # TODO: 4. Вернуть HabitMarkResponse

    habit_marked = services.mark_habit(habit_id=habit_id)
    last_date = habit_marked.marks[-1]
    last_date_formated = last_date.strftime('%Y-%m-%d')
    res_habit = HabitMarkResponse(id=habit_marked.id, name=habit_marked.name, last_marked_at=last_date_formated)

    return res_habit



@router.get("/habits/", response_model=List[HabitListResponse])
def get_all_habits():
    """Получить список всех привычек."""
    # TODO: 1. Вызвать services.get_all_habits()
    # TODO: 2. Для каждой привычки создать HabitListResponse
    # TODO: 3. Преобразовать dates в список строк формата YYYY-MM-DD
    # TODO: 4. Вернуть список
    habits = services.get_all_habits()
    result = []
    for habit in habits:
        marks_str = [mark.strftime('%Y-%m-%d') for mark in habit.marks]
        habit_response = HabitListResponse(
            id=habit.id,
            name=habit.name,
            marks=marks_str
        )
        result.append(habit_response)
    
    return result
