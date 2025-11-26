from typing import List
from fastapi import APIRouter, HTTPException, status
from habit_tracker.core import services
from habit_tracker.core.models import (
    HabitCreate,
    HabitUpdate,
    HabitBase,
    HabitResponse,
    HabitMarkResponse
)

router = APIRouter()


@router.post("/", response_model=HabitBase, status_code=status.HTTP_201_CREATED)
def create_habit(habit: HabitCreate):
    """Создать новую привычку."""
    try:
        new_habit = services.create_habit(habit)
        return HabitBase(id=new_habit.id, name=new_habit.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[HabitResponse])
def get_all_habits():
    """Получить список всех привычек с деталями."""
    habits_data = services.get_all_habits_with_details()
    return [HabitResponse(**habit) for habit in habits_data]


@router.get("/{habit_id}/", response_model=HabitResponse)
def get_habit(habit_id: int):
    """Получить одну привычку по ID."""
    habit_data = services.get_habit_by_id_with_details(habit_id)
    if habit_data is None:
        raise HTTPException(status_code=404, detail="Habit not found.")
    return HabitResponse(**habit_data)


@router.put("/{habit_id}/", response_model=HabitBase)
def update_habit(habit_id: int, habit_update: HabitUpdate):
    """Обновить привычку по ID."""
    try:
        updated_habit = services.update_habit(habit_id, habit_update)
        if updated_habit is None:
            raise HTTPException(status_code=404, detail="Habit not found.")
        return HabitBase(id=updated_habit.id, name=updated_habit.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{habit_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: int):
    """Удалить привычку по ID."""
    success = services.delete_habit(habit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Habit not found.")
    return


@router.post("/{habit_id}/mark/", response_model=HabitMarkResponse)
def mark_habit(habit_id: int):
    """Отметить выполнение привычки за TODAY."""
    try:
        result = services.mark_habit(habit_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Habit not found.")
        return HabitMarkResponse(
            id=result["id"],
            name=result["name"],
            last_marked_at=result["last_marked_at"],
            streak=result["streak"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
