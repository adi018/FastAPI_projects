from fastapi import APIRouter
from pydantic import BaseModel
from models import Users  # Assuming you have a User model defined in models.py
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from typing import Annotated



router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    """
    Request model for creating a new user.
    This model defines the structure of the request body for creating a new user.
    """
    username: str
    email: str
    first_name: str 
    last_name: str 
    password: str
    role:str



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

@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):   
    """
    Endpoint to get user information.
    This endpoint retrieves user information.
    """
    create_user_model = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password), 
        role=create_user_request.role,
        is_active=True 
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)