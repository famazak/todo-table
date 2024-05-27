import pytest
from todo_table.todo import Todo, Todos


@pytest.fixture
def todos():
    todo1 = Todo(
        name="Buy milk", created_at="2024-05-25 10:00:00", due_date="2024-05-26"
    )
    todo2 = Todo(name="Write code", created_at="2024-05-25 11:00:00")
    todos = Todos(todos=[todo1, todo2])
    return todos
