from todo_table.fire_cli import TodoTableCLI
from todo_table.database import write_todos_to_file
from todo_table.todo import Todos, Todo
from pathlib import Path
import json


TEST_TODO_TABLE_FILE = Path("tests/dummy_path.json")


def test_cli_init(todo_table_cli: TodoTableCLI):
    empty_todos: dict[str, list] = {"todos": []}
    todo_table_cli.init(database_file=TEST_TODO_TABLE_FILE)

    with TEST_TODO_TABLE_FILE.open(encoding="utf-8") as file:
        test_init_todos = json.load(file)

    assert empty_todos == test_init_todos


def test_cli_add(todo_table_cli: TodoTableCLI):
    # call init to reset the test file
    todo_table_cli.init(database_file=TEST_TODO_TABLE_FILE)

    test_todos = {"todos": [{"name": "test todo", "created_at": "2024-05-31 12:00:00"}]}
    todo_table_cli.add(name="test todo", database_file=TEST_TODO_TABLE_FILE)

    with TEST_TODO_TABLE_FILE.open(encoding="utf-8") as file:
        test_add_todos = json.load(file)

    assert test_todos["todos"][0]["name"] == test_add_todos["todos"][0]["name"]


def test_cli_add_with_due_date(mocker, todos: Todos, todo_table_cli: TodoTableCLI):
    # call init to reset the test file
    todo_table_cli.init(database_file=TEST_TODO_TABLE_FILE)
    mocker.patch("todo_table.database.load_todos_from_file", return_value=todos)

    todo_table_cli.add(
        name="this is a test", due="2024-08-01", database_file=TEST_TODO_TABLE_FILE
    )

    with TEST_TODO_TABLE_FILE.open(encoding="utf-8") as file:
        test_add_todos = json.load(file)

    added_todo = next(
        (
            todo
            for todo in test_add_todos["todos"]
            if todo["name"] == "this is a test" and todo["due_date"] == "2024-08-01"
        ),
        None,
    )

    assert added_todo is not None


def test_cli_done(mocker, todos: Todos, todo_table_cli: TodoTableCLI, todo: Todo):
    mocker.patch("todo_table.database.load_todos_from_file", return_value=todos)
    mocker.patch("todo_table.todo.fetch_todo", return_value=todo)

    deleted_todo = todo_table_cli.done(id=1, database_file=TEST_TODO_TABLE_FILE)

    assert deleted_todo is not None


def test_cli_done_bad_id(
    mocker, todos: Todos, todo_table_cli: TodoTableCLI, todo: Todo
):
    mocker.patch("todo_table.database.load_todos_from_file", return_value=todos)
    mocker.patch("todo_table.todo.fetch_todo", return_value=None)

    deleted_todo = todo_table_cli.done(id=8, database_file=TEST_TODO_TABLE_FILE)

    assert deleted_todo is None
