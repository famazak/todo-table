import pytest
from todo_table.todo import Todo, Todos


# Helper function to mock current time for testing
def mock_current_time() -> str:
    return "2024-05-26 12:00:00"


@pytest.fixture
def todos():
    todo1 = Todo(
        name="Buy milk", created_at="2024-05-25 10:00:00", due_date="2024-05-26"
    )
    todo2 = Todo(name="Write code", created_at="2024-05-25 11:00:00")
    todos = Todos(todos=[todo1, todo2])
    return todos


# Mocking the default factory function for Todo
@pytest.fixture(autouse=True)
def mock_current_time_formatted(monkeypatch):
    monkeypatch.setattr("todo_table.todo.current_time_formatted", mock_current_time)
