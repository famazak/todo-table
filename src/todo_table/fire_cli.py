from typing import Optional
import fire
from todo_table.todo import Todo, Todos, current_time_formatted, fetch_todo
from todo_table.database import write_todos_to_file, load_todos_from_file
from pathlib import Path
from prettytable import PrettyTable

TODO_TABLE_FILE = Path.home() / "todo_table.json"


class TodoTableCLI:
    def init(self) -> None:
        init_todos = Todos(todos=[])
        write_todos_to_file(todos=init_todos, todos_file=TODO_TABLE_FILE)

    def add(self, name: str, due: Optional[str] = None) -> None:
        todo = Todo(name=name, due_date=due)

        todos = load_todos_from_file(todos_file=TODO_TABLE_FILE)
        todos.todos.append(todo)

        write_todos_to_file(todos=todos, todos_file=TODO_TABLE_FILE)

    def done(self, id: int) -> None:
        offset_id = id - 1  # to offset adding 1 to the index in show
        todos = load_todos_from_file(todos_file=TODO_TABLE_FILE)
        todo = fetch_todo(todos=todos, id=offset_id)
        if todo is not None:
            del todos.todos[offset_id]
            print(f"Todo {todo.name} completed")
            write_todos_to_file(todos=todos, todos_file=TODO_TABLE_FILE)
        else:
            print(f"No todo with ID {str(id)} found")

    def show(self) -> None:
        table = PrettyTable()
        table.field_names = ["Id", "Name", "Created At", "Completed At", "Due Date"]

        todos = load_todos_from_file(todos_file=TODO_TABLE_FILE)

        for index, todo in enumerate(todos.todos):
            table_index = index + 1  # so the ids start at 1
            table.add_row(
                [
                    table_index,
                    todo.name,
                    todo.created_at,
                    todo.completed_at,
                    todo.due_date,
                ]
            )

        print(table)


def fire_cli() -> None:
    todo_table = TodoTableCLI()
    fire.Fire(todo_table)
