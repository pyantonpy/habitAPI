from typing import List
from fastapi import APIRouter, status
from habit_tracker.core import services
from habit_tracker.core.models import (
    HabitCreate,
    HabitUpdate,
    HabitBase,
    HabitResponse,
    HabitMarkResponse,
    HabitStatsResponse
)

router = APIRouter()


@router.post("/", response_model=HabitBase, status_code=status.HTTP_201_CREATED)
async def create_habit(habit: HabitCreate):
    new_habit = services.create_habit(habit)
    return HabitBase(id=new_habit.id, name=new_habit.name)


@router.get("/", response_model=List[HabitResponse])
async def get_all_habits():
    habits = services.get_all_habits()
    return [
        HabitResponse(
            id=habit.id,
            name=habit.name,
            streak=services.calculate_streak(habit.marks),
            marks=habit.marks
        )
        for habit in habits
    ]


@router.get("/{habit_id}/", response_model=HabitResponse)
async def get_habit(habit_id: int):
    habit = services.get_habit_by_id(habit_id)
    return HabitResponse(
        id=habit.id,
        name=habit.name,
        streak=services.calculate_streak(habit.marks),
        marks=habit.marks
    )


@router.put("/{habit_id}/", response_model=HabitBase)
async def update_habit(habit_id: int, habit_update: HabitUpdate):
    updated_habit = services.update_habit(habit_id, habit_update)
    return HabitBase(id=updated_habit.id, name=updated_habit.name)


@router.delete("/{habit_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(habit_id: int):
    services.delete_habit(habit_id)
    return


@router.post("/{habit_id}/mark/", response_model=HabitMarkResponse)
async def mark_habit(habit_id: int):
    habit = services.mark_habit_completed(habit_id)
    last_marked_at = habit.marks[-1] if habit.marks else None
    return HabitMarkResponse(
        id=habit.id,
        name=habit.name,
        last_marked_at=last_marked_at,
        streak=services.calculate_streak(habit.marks)
    )


@router.get("/{habit_id}/stats/", response_model=HabitStatsResponse)
async def get_habit_stats(habit_id: int):
    habit = services.get_habit_by_id(habit_id)
    stats = services.calculate_habit_stats(habit)
    return HabitStatsResponse(
        id=habit.id,
        name=habit.name,
        total_marks=stats["total_marks"],
        current_streak=stats["current_streak"],
        max_streak=stats["max_streak"],
        success_rate=stats["success_rate"],
        last_dates=stats["last_dates"]
    )