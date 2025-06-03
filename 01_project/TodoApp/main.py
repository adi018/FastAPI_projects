from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos # Import the auth router from the routers module

# Initialize the FastAPI application
app = FastAPI()

# Create the database tables based on the models defined in the models module
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)  # Include the router for models
app.include_router(todos.router)  # Include the router for todos
