from datetime import date
from typing import Dict, List
from fastapi import HTTPException
from habit_tracker.core.models import Habit

# In-memory хранилище
habits_db: Dict[int, Habit] = {} # "для себя" словарь, где ключи целые числа, а 
_next_id = 1                     # значения типа класса Habit


def create_habit(name: str) -> Habit:
    """Создать новую привычку."""
    global _next_id
    
    # TODO: 1. Проверить, что name не пустое
    #          Если пустое - raise HTTPException(status_code=400, detail="Habit name cannot be empty.")
    
    # TODO: 2. Проверить, что привычка с таким именем не существует
    #          Если существует - raise HTTPException(status_code=400, detail="Habit with this name already exists.")
    
    # TODO: 3. Создать объект Habit с текущим _next_id и name
    
    # TODO: 4. Сохранить в habits_db
    
    # TODO: 5. Увеличить _next_id
    
    # TODO: 6. Вернуть созданную привычку
    if not name.strip():
        raise HTTPException(status_code=400, detail="Habit name cannot be empty.")
    
    if any(habit.name == name for habit in habits_db.values()):
        raise HTTPException(status_code=400, detail="Habit with this name already exists.")
    
    new_habbit = Habit(_next_id, name)
    habits_db[_next_id] = new_habbit
    _next_id += 1

    return new_habbit


def mark_habit(habit_id: int) -> Habit:
    """Отметить выполнение привычки за текущий день."""
    
    # TODO: 1. Получить привычку из habits_db по habit_id
    #          Если не найдена - raise HTTPException(status_code=404, detail="Habit not found.")
    
    # TODO: 2. Получить сегодняшнюю дату (date.today())
    
    # TODO: 3. Проверить, что today не в habit.marks
    #          Если уже есть - raise HTTPException(status_code=400, detail="Habit already marked for today.")
    
    # TODO: 4. Добавить today в habit.marks
    
    # TODO: 5. Вернуть обновленную привычку
    if not habit_id in habits_db.keys():
        raise HTTPException(status_code=404, detail="Habit not found.")
    
    date_today = date.today()
    habit_tracked = habits_db[habit_id]

    if date_today in habit_tracked.marks:
        raise HTTPException(status_code=400, detail="Habit already marked for today.")
    
    habit_tracked.marks.append(date_today)

    return habit_tracked


def get_all_habits() -> List[Habit]:
    """Получить список всех привычек."""
    # TODO: Вернуть список всех привычек из habits_db
    return list(habits_db.values())
