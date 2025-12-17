from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from habit_tracker.views import web
from habit_tracker.api import habits_api
from habit_tracker.core.exceptions import (
    HabitNotFoundException,
    HabitAlreadyMarkedTodayException,
    HabitNameConflictException,
    InvalidInputException,
)


app = FastAPI(title="Habit Tracker API")
app.mount("/static", StaticFiles(directory="habit_tracker/static"), name="static")
app.include_router(web.router, tags=["Web Interface"])
app.include_router(habits_api.router, prefix="/api/habits", tags=["Habits API"])


@app.exception_handler(HabitNotFoundException)
async def habit_not_found_exception_handler(request: Request, exc: HabitNotFoundException):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return RedirectResponse(url="/?error=" + exc.detail, status_code=303)


@app.exception_handler(HabitAlreadyMarkedTodayException)
async def habit_already_marked_today_exception_handler(request: Request, exc: HabitAlreadyMarkedTodayException):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return RedirectResponse(url="/?error=" + exc.detail, status_code=303)


@app.exception_handler(HabitNameConflictException)
async def habit_name_conflict_exception_handler(request: Request, exc: HabitNameConflictException):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return RedirectResponse(url="/?error=" + exc.detail, status_code=303)


@app.exception_handler(InvalidInputException)
async def invalid_input_exception_handler(request: Request, exc: InvalidInputException):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return RedirectResponse(url="/?error=" + exc.detail, status_code=303)