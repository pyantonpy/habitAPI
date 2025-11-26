from fastapi import APIRouter, Request, HTTPException, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from habit_tracker.core.services import (
    get_all_habits_with_details,
    get_habit_by_id_with_details,
    create_habit,
    mark_habit,
    update_habit,
    delete_habit,
    is_habit_marked_today,
)
from habit_tracker.core.models import HabitCreate, HabitUpdate

router = APIRouter()

templates = Jinja2Templates(directory="habit_tracker/templates")


@router.get("/", name="main-page")
def main_page(request: Request):
    habits = get_all_habits_with_details()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "habits": habits,
            "is_marked_today": is_habit_marked_today,
        }
    )


@router.get("/habit/{habit_id}/", name="habit-detail")
def habit_detail(request: Request, habit_id: int):
    habit = get_habit_by_id_with_details(habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Привычка не найдена")
    return templates.TemplateResponse(
        request=request,
        name="habit_detail.html",
        context={"habit": habit}
    )


@router.post("/habit/add", name="add_habit_from_form")
def add_habit_from_form(name: str = Form(...)):
    try:
        habit_data = HabitCreate(name=name)
        create_habit(habit_data)
    except ValueError:
        pass
    return RedirectResponse(
        url=router.url_path_for("main-page"),
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/habit/{habit_id}/mark", name="mark_habit_from_form")
def mark_habit_from_form(habit_id: int):
    try:
        mark_habit(habit_id)
    except ValueError:
        pass
    return RedirectResponse(
        url=router.url_path_for("main-page"),
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/habit/{habit_id}/edit", name="edit_habit_from_form")
def edit_habit_from_form(habit_id: int, name: str = Form(...)):
    try:
        habit_data = HabitUpdate(name=name)
        updated = update_habit(habit_id, habit_data)
        if updated is None:
            raise HTTPException(status_code=404, detail="Привычка не найдена")
    except ValueError:
        pass
    return RedirectResponse(
        url=router.url_path_for("habit-detail", habit_id=habit_id),
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/habit/{habit_id}/delete", name="delete_habit_from_form")
def delete_habit_from_form(habit_id: int):
    delete_habit(habit_id)
    return RedirectResponse(
        url=router.url_path_for("main-page"),
        status_code=status.HTTP_303_SEE_OTHER
    )