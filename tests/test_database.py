import json
import pytest
from todo_table.database import write_todos_to_file, load_todos_from_file
from todo_table.todo import Todos
from pathlib import Path


def test_write_todos_to_file_success(mocker, todos):
    todos_file = Path("tests/dummy_path.json")
    mock_open = mocker.patch("pathlib.Path.open", mocker.mock_open())

    write_todos_to_file(todos, todos_file)

    mock_open.assert_called_once_with("w", encoding="utf-8")
    mock_open().write.assert_called_once_with(todos.model_dump_json())


def test_write_todos_to_file_correct_data(todos):
    todos_file = Path("tests/dummy_path.json")
    write_todos_to_file(todos, todos_file)

    with todos_file.open("r", encoding="utf-8") as file:
        loaded_todos = Todos(**json.load(file))

    assert loaded_todos == todos


def test_load_todos_from_file_success(mocker):
    todos_file = Path("tests/dummy_path.json")
    todos_json = {
        "todos": [
            {
                "name": "Buy milk",
                "created_at": "2024-05-25 10:00:00",
                "due_date": "2024-05-26",
            },
            {"name": "Write code", "created_at": "2024-05-25 11:00:00"},
        ]
    }

    mock_open = mocker.patch(
        "pathlib.Path.open", mocker.mock_open(read_data=json.dumps(todos_json))
    )

    todos = load_todos_from_file(todos_file)

    mock_open.assert_called_once_with("r", encoding="utf-8")
    assert len(todos.todos) == 2
    assert todos.todos[0].name == "Buy milk"
    assert todos.todos[1].name == "Write code"


def test_load_todos_from_file_not_found(mocker):
    todos_file = Path("tests/dummy_path.json")
    mocker.patch("pathlib.Path.open", side_effect=FileNotFoundError)
    mock_print = mocker.patch("builtins.print")

    with pytest.raises(SystemExit):
        load_todos_from_file(todos_file)

    mock_print.assert_called_once_with("No todo file found, you need to add a todo!")
