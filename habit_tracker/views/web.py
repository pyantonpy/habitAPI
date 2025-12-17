from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from habit_tracker.core.services import (
    get_all_habits,
    get_habit_by_id,
    create_habit,
    mark_habit_completed,
    update_habit,
    delete_habit,
    calculate_habit_stats,
)
from habit_tracker.core.models import HabitCreate, HabitUpdate

router = APIRouter()

templates = Jinja2Templates(directory="habit_tracker/templates")


@router.get("/", name="main-page")
async def main_page(request: Request):
    habits = get_all_habits()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "habits": [
                {
                    "id": habit.id,
                    "name": habit.name,
                    "marks": habit.marks,
                    "streak": calculate_streak(habit.marks),
                    "marked_today": TODAY in habit.marks,
                }
                for habit in habits
            ],
            "is_marked_today": lambda habit_id: TODAY in get_habit_by_id(habit_id).marks,
        }
    )


@router.get("/habit/{habit_id}/", name="habit-detail")
async def habit_detail(request: Request, habit_id: int):
    habit = get_habit_by_id(habit_id)
    return templates.TemplateResponse(
        request=request,
        name="habit_detail.html",
        context={
            "habit": {
                "id": habit.id,
                "name": habit.name,
                "marks": habit.marks,
                "streak": calculate_streak(habit.marks),
                "marked_today": TODAY in habit.marks,
            }
        }
    )


@router.post("/habit/add", name="add_habit_from_form")
async def add_habit_from_form(name: str = Form(...)):
    habit_data = HabitCreate(name=name)
    create_habit(habit_data)
    return RedirectResponse(
        url=router.url_path_for("main-page"),
        status_code=303
    )


@router.post("/habit/{habit_id}/mark", name="mark_habit_from_form")
async def mark_habit_from_form(habit_id: int):
    mark_habit_completed(habit_id)
    return RedirectResponse(
        url=router.url_path_for("main-page"),
        status_code=303
    )


@router.post("/habit/{habit_id}/edit", name="edit_habit_from_form")
async def edit_habit_from_form(habit_id: int, name: str = Form(...)):
    habit_data = HabitUpdate(name=name)
    update_habit(habit_id, habit_data)
    return RedirectResponse(
        url=router.url_path_for("habit-detail", habit_id=habit_id),
        status_code=303
    )


@router.post("/habit/{habit_id}/delete", name="delete_habit_from_form")
async def delete_habit_from_form(habit_id: int):
    delete_habit(habit_id)
    return RedirectResponse(
        url=router.url_path_for("main-page"),
        status_code=303
    )


@router.get("/stats/", response_class=HTMLResponse, name="stats-page")
async def get_stats_page(request: Request):
    habits = get_all_habits()
    stats_data = []
    for habit in habits:
        stats = calculate_habit_stats(habit)
        stats_data.append({
            "id": habit.id,
            "name": habit.name,
            "total_marks": stats["total_marks"],
            "current_streak": stats["current_streak"],
            "max_streak": stats["max_streak"],
            "success_rate": stats["success_rate"],
            "last_dates": stats["last_dates"],
        })
    return templates.TemplateResponse(
        request=request,
        name="stats.html",
        context={"stats": stats_data}
    )


from datetime import date

TODAY = date(2025, 7, 12)


def calculate_streak(marks):
    if not marks:
        return 0
    unique_dates = sorted(set(marks), reverse=True)
    if unique_dates[0] < TODAY - date.resolution:
        return 0
    streak = 0
    current_date = TODAY
    i = 0
    while current_date >= min(unique_dates):
        if i < len(unique_dates) and unique_dates[i] == current_date:
            streak += 1
            i += 1
        elif current_date == TODAY:
            return 0
        else:
            break
        current_date -= date.resolution
    return streak