from pydantic import BaseModel, Field, ConfigDict

from storage.todos import Todos

class User(BaseModel):
    username: str
    password: str
    todos: Todos = Field(default_factory=Todos)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class UserWithoutPassword(BaseModel):
    username: str
    todo_count: int