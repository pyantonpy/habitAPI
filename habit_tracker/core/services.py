from datetime import date
from typing import Dict, List, Optional
from habit_tracker.core.models import Habit, HabitCreate, HabitUpdate

TODAY = date(2025, 7, 12)

habits_db: Dict[int, Habit] = {
    1: Habit(id=1, name="Бег", marks=[date(2025, 7, 10), date(2025, 7, 11)]),
    2: Habit(id=2, name="Чтение", marks=[date(2025, 7, 11)]),
    3: Habit(id=3, name="Медитация", marks=[]),
}
_next_habit_id = 4


def calculate_streak(marks: List[date]) -> int:
    if not marks:
        return 0

    unique_dates = sorted(set(marks), reverse=True)
    streak = 0
    current_date = TODAY

    if unique_dates[0] < TODAY - date.resolution:
        return 0

    i = 0
    while current_date >= min(unique_dates):
        if i < len(unique_dates) and unique_dates[i] == current_date:
            streak += 1
            i += 1
        elif current_date == TODAY:
            if i < len(unique_dates) and unique_dates[i] == TODAY - date.resolution:
                current_date = TODAY - date.resolution
                streak += 1
                i += 1
                continue
            else:
                return 0
        else:
            break
        current_date -= date.resolution

    return streak


def get_all_habits_with_details() -> List[dict]:
    habits = [] 
    for habit in sorted(habits_db.values(), key=lambda h: h.id):
        streak = calculate_streak(habit.marks)
        habits.append({
            "id": habit.id,
            "name": habit.name,
            "marks": habit.marks,
            "streak": streak,
        })
    return habits


def get_habit_by_id_with_details(habit_id: int) -> Optional[dict]:
    habit = habits_db.get(habit_id)
    if habit is None:
        return None
    streak = calculate_streak(habit.marks)
    return {
        "id": habit.id,
        "name": habit.name,
        "marks": habit.marks,
        "streak": streak,
    }


def create_habit(habit_data: HabitCreate) -> Habit:
    name = habit_data.name.strip()
    if not name:
        raise ValueError("Habit name cannot be empty.")
    if any(h.name == name for h in habits_db.values()):
        raise ValueError("Habit with this name already exists.")

    global _next_habit_id
    new_habit = Habit(id=_next_habit_id, name=name)
    habits_db[_next_habit_id] = new_habit
    _next_habit_id += 1
    return new_habit


def update_habit(habit_id: int, habit_data: HabitUpdate) -> Optional[Habit]:
    habit = habits_db.get(habit_id)
    if habit is None:
        return None

    new_name = habit_data.name.strip()
    if not new_name:
        raise ValueError("Habit name cannot be empty.")
    if any(h.id != habit_id and h.name == new_name for h in habits_db.values()):
        raise ValueError("Habit with this name already exists.")

    habit.name = new_name
    return habit


def delete_habit(habit_id: int) -> bool:
    if habit_id in habits_db:
        del habits_db[habit_id]
        return True
    return False


def mark_habit(habit_id: int) -> Optional[dict]:
    habit = habits_db.get(habit_id)
    if habit is None:
        return None

    if TODAY in habit.marks:
        raise ValueError("Habit already marked for today.")

    habit.marks.append(TODAY)
    streak = calculate_streak(habit.marks)
    return {
        "id": habit.id,
        "name": habit.name,
        "last_marked_at": TODAY.isoformat(),
        "streak": streak,
    }


def is_habit_marked_today(habit_id: int) -> bool:
    habit = habits_db.get(habit_id)
    if habit is None:
        return False
    return TODAY in habit.marks 