from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    priority: int