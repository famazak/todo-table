import pytest
from todo_table.todo import Todo


def test_validate_date_format_valid():
    # with a valid due_date, no exception should be raised by the validator
    todo = Todo(name="Test Todo", due_date="2024-06-01")
    assert todo.due_date == "2024-06-01"


def test_validate_date_format_invalid():
    with pytest.raises(ValueError) as exc_info:
        Todo(
            name="Test Todo",
            due_date="2024-06-01T12:00:00",  # Invalid date format
        )
    assert "Due date must be in the format YYYY-MM-DD" in str(exc_info.value)


def test_optional_fields():
    todo = Todo(name="Test Todo")
    assert todo.completed_at is None
    assert todo.due_date is None
