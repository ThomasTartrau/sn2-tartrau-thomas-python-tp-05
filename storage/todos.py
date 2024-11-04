from typing import Dict, ClassVar
from pydantic import BaseModel
import uuid
from model.todo import Todo

class Todos(BaseModel):
    todos: ClassVar[Dict[str, Todo]] = {}  # Ajout du type `Dict[str, Todo]` avec `ClassVar`
    
    def __init__(self) -> None:
        pass

    def add(self, todo: Todo):
        id = str(uuid.uuid4())
        todo.id = id
        self.todos[id] = todo.dict()

    def get_by_id(self, id: str):
        return self.todos.get(id)
    
    def get_all(self):
        return self.todos
    
    def get_length(self):
        return len(self.todos)
    
    def sort_by_priority(self):
        return sorted(self.todos.values(), key=lambda x: x["priority"])
    
    def update(self, id: str, todo: Todo):
        todo.id = id
        self.todos[id] = todo

    def delete(self, id: str):
        if self.todos.get(id):
            del self.todos[id]
            return True
        return False
