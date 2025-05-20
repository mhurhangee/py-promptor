"""Database models for Promptor."""
import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import Session

from lib.db.database import Base


class Prompt(Base):
    """Prompt model for storing user prompts."""

    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text)
    category = Column(String(100), index=True)
    user_id = Column(String(50), index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    @classmethod
    def create(
        cls,
        db: Session,
        title: str,
        content: str,
        user_id: str,
        category: Optional[str] = None,
    ) -> "Prompt":
        """Create a new prompt."""
        prompt = cls(
            title=title,
            content=content,
            category=category or "General",
            user_id=user_id,
        )
        db.add(prompt)
        db.commit()
        db.refresh(prompt)
        return prompt

    @classmethod
    def get_by_id(cls, db: Session, prompt_id: int) -> Optional["Prompt"]:
        """Get a prompt by ID."""
        return db.query(cls).filter(cls.id == prompt_id).first()

    @classmethod
    def get_all_by_user(cls, db: Session, user_id: str) -> list:
        """Get all prompts for a user."""
        return db.query(cls).filter(cls.user_id == user_id).order_by(cls.title).all()

    @classmethod
    def delete(cls, db: Session, prompt_id: int) -> bool:
        """Delete a prompt."""
        prompt = cls.get_by_id(db, prompt_id)
        if prompt:
            db.delete(prompt)
            db.commit()
            return True
        return False
