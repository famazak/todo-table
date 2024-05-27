from datetime import datetime
from itertools import count
from typing import Optional
from pydantic import BaseModel, Field, validator


def current_time_formatted() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


class Todo(BaseModel):
    name: str
    created_at: str = Field(default_factory=current_time_formatted)
    completed_at: Optional[str] = None
    due_date: Optional[str] = None

    @validator("due_date")
    def validate_date_format(cls, due_date_value: Optional[str]) -> Optional[str]:
        if due_date_value is not None:
            try:
                datetime.strptime(due_date_value, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Due date must be in the format YYYY-MM-DD")

        return due_date_value


class Todos(BaseModel):
    todos: list[Todo]


def fetch_todo(todos: Todos, id: int) -> Optional[Todo]:
    for index, todo in enumerate(todos.todos):
        if index == id:
            return todo

    return None
