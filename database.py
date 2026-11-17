
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./alerts.db")

connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)


# Create the database engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

# Create database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for database models
Base = declarative_base()
