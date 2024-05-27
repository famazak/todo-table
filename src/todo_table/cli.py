from typing import Optional
import click
from todo_table.database import write_todos_to_file, load_todos_from_file
from todo_table.todo import Todo, Todos
from pathlib import Path

TODO_TABLE_FILE = Path.home() / "todo_table.json"


@click.group()
def cli():
    pass


@click.command()
def init():
    init_todos = Todos(todos=[])
    write_todos_to_file(todos=init_todos, todos_file=TODO_TABLE_FILE)


@click.command()
@click.option("--due", "-d", default=None, type=str)
@click.argument("name", type=str)
def add(name, due) -> None:
    todo = Todo(name=name, due_date=due)

    todos = load_todos_from_file(todos_file=TODO_TABLE_FILE)
    todos.todos.append(todo)

    write_todos_to_file(todos=todos, todos_file=TODO_TABLE_FILE)


@click.command()
def done():
    pass


cli.add_command(init)
cli.add_command(add)
cli.add_command(done)
