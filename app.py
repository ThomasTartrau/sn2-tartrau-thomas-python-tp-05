from model.user import User, UserWithoutPassword
from model.token import Token
from model.todo import Todo
from security.jwt import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from db import users

from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status

app = FastAPI(description="TP5 API")

@app.get("/")
def root():
    return {}

@app.get("/miscellaneous/addition")
def addition(a: int, b: int):
    return {"result": a + b}

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    hashed_password = users.get_password_hash(user.password)
    user.password = hashed_password
    if users.add(user):
        return UserWithoutPassword(username=user.username, todo_count=len(user.todos.todos))
    raise HTTPException(status_code=400, detail="User already exists")

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me/", response_model=UserWithoutPassword)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return UserWithoutPassword(username=current_user.username, todo_count=len(current_user.todos.todos))

@app.post("/users/me/todo", response_model=Todo ,status_code=status.HTTP_201_CREATED)
async def create_todo(todo: Todo, current_user: User = Depends(get_current_user)):
    current_user.todos.add(todo)
    return todo

@app.get("/users/me/todo", response_model=list[Todo])
async def read_todos(current_user: User = Depends(get_current_user)):
    return current_user.todos.sort_by_priority()

@app.patch("/users/me/todo/{id}", response_model=Todo)
async def update_todo(id: str, todo: Todo, current_user: User = Depends(get_current_user)):
    current_user.todos.update(id, todo)
    return todo

@app.delete("/users/me/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: str, current_user: User = Depends(get_current_user)):
    if current_user.todos.delete(id):
        return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")