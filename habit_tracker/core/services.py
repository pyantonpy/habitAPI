from datetime import date
from typing import List, Dict
from habit_tracker.core.models import Habit, HabitCreate, HabitUpdate
from habit_tracker.core.exceptions import (
    HabitNotFoundException,
    HabitAlreadyMarkedTodayException,
    HabitNameConflictException,
    InvalidInputException,
)

TODAY = date(2025, 7, 12)

habits_db: Dict[int, Habit] = {
    1: Habit(id=1, name="Бег", marks=[date(2025, 7, 10), date(2025, 7, 11)]),
    2: Habit(id=2, name="Чтение", marks=[date(2025, 7, 11)]),
    3: Habit(id=3, name="Медитация", marks=[]),
}
_next_habit_id = 4


def calculate_streak(marks: List[date]) -> int:
    """Вычисляет текущий streak (серия дней подряд, включая сегодня)."""
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


def calculate_max_streak(marks: List[date]) -> int:
    """Вычисляет максимальный streak за всё время."""
    if not marks:
        return 0

    unique_dates = sorted(set(marks))
    max_streak = 1
    current_streak = 1

    for i in range(1, len(unique_dates)):
        if unique_dates[i] - unique_dates[i - 1] == date.resolution:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1

    return max_streak


def calculate_habit_stats(habit: Habit) -> dict:
    """Вычисляет полную статистику привычки."""
    total_marks = len(habit.marks)

    if total_marks == 0:
        return {
            "total_marks": total_marks,
            "current_streak": 0,
            "max_streak": 0,
            "success_rate": 0.0,
            "last_dates": [],
        }

    current_streak = calculate_streak(habit.marks)
    max_streak = calculate_max_streak(habit.marks)

    first_mark = min(habit.marks)
    days_since_start = (TODAY - first_mark).days + 1
    success_rate = round((total_marks / days_since_start) * 100, 2)

    last_dates = sorted(set(habit.marks), reverse=True)[:5]

    return {
        "total_marks": total_marks,
        "current_streak": current_streak,
        "max_streak": max_streak,
        "success_rate": success_rate,
        "last_dates": last_dates,
    }


def get_habit_by_id(habit_id: int) -> Habit:
    """Возвращает привычку по ID. Выбрасывает исключение, если не найдена."""
    habit = habits_db.get(habit_id)
    if habit is None:
        raise HabitNotFoundException()
    return habit


def get_all_habits() -> List[Habit]:
    """Возвращает список всех привычек, отсортированных по ID."""
    return sorted(habits_db.values(), key=lambda h: h.id)


def create_habit(habit_data: HabitCreate) -> Habit:
    """Создаёт новую привычку."""
    name = habit_data.name.strip()
    if not name:
        raise InvalidInputException("Habit name cannot be empty.")

    if any(h.name == name for h in habits_db.values()):
        raise HabitNameConflictException()

    global _next_habit_id
    new_habit = Habit(id=_next_habit_id, name=name)
    habits_db[_next_habit_id] = new_habit
    _next_habit_id += 1
    return new_habit


def update_habit(habit_id: int, habit_data: HabitUpdate) -> Habit:
    """Обновляет существующую привычку."""
    habit = get_habit_by_id(habit_id)

    new_name = habit_data.name.strip()
    if not new_name:
        raise InvalidInputException("Habit name cannot be empty.")

    if any(h.id != habit_id and h.name == new_name for h in habits_db.values()):
        raise HabitNameConflictException()

    habit.name = new_name
    return habit


def delete_habit(habit_id: int) -> None:
    """Удаляет привычку по ID."""
    if habit_id not in habits_db:
        raise HabitNotFoundException()
    del habits_db[habit_id]


def mark_habit_completed(habit_id: int) -> Habit:
    """Отмечает привычку как выполненную за сегодня."""
    habit = get_habit_by_id(habit_id)

    if TODAY in habit.marks:
        raise HabitAlreadyMarkedTodayException()

    habit.marks.append(TODAY)
    return habit