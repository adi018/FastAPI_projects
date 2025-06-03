from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# This URL is used to connect to the SQLite database for the Todo application.
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)  # SQLite specific argument to allow multiple threads to access the database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()