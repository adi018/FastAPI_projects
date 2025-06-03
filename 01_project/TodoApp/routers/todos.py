from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
import models
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated


# Initialize the FastAPI application
router = APIRouter()



def get_db():
    """
    Dependency to get a database session.
    This function is used to create a new database session for each request.
    """
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Yield the session to the caller
    finally:
        db.close()  # Close the session after use

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    """
    Request model for creating a new todo item.
    This model defines the structure of the request body for creating a new todo item.
    """
    title: str = Field(min_length=3)
    description: str = Field(min_length = 1, max_length = 100)
    priority: int = Field(gt=0, lt=6)
    completed: bool = Field(default=False)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    """
    Endpoint to read all todo items.
    This endpoint retrieves all todo items from the database.
    """
    todos = db.query(models.TodoItem).all()
    return todos

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    """
    Endpoint to read a specific todo item by its ID.
    This endpoint retrieves a todo item from the database based on the provided ID.
    """
    todo = db.query(models.TodoItem).filter(models.TodoItem.id == todo_id).first()
    if todo is not None:
        return todo
    return HTTPException(status_code=404, detail="Todo item not found")

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: TodoRequest, db: db_dependency):
    """
    Endpoint to create a new todo item.
    This endpoint adds a new todo item to the database based on the provided request body."""
    print(todo_request)
    print(todo_request.dict())
    todo_model = models.TodoItem(**(todo_request.dict()))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(todo_request: TodoRequest, db: db_dependency, todo_id: int = Path(gt=0)):
    """
    Endpoint to update an existing todo item.
    This endpoint updates a todo item in the database based on the provided ID and request body.
    """
    todo_model = db.query(models.TodoItem).filter(models.TodoItem.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    
    for key, value in todo_request.dict().items():
        setattr(todo_model, key, value)
    
    db.commit()
    db.refresh(todo_model)

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    """
    Endpoint to delete a todo item by its ID.
    This endpoint removes a todo item from the database based on the provided ID.
    """
    todo_model = db.query(models.TodoItem).filter(models.TodoItem.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    
    db.delete(todo_model)
    db.commit()