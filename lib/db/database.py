"""Database setup for Promptor."""
import os
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# Create data directory if it doesn't exist
data_dir = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data"))
data_dir.mkdir(exist_ok=True)

# Database setup
SQLALCHEMY_DATABASE_URL = f"sqlite:///{data_dir}/promptor.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize the database."""
    # Import all models here to ensure they are registered with the Base
    from lib.db.models import Prompt  # noqa: F401

    Base.metadata.create_all(bind=engine)
