"""Database models for Promptor."""
import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import Session

from lib.db.database import Base


class Prompt(Base):
    """Prompt model for storing user prompts."""

    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True, index=True)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=True, index=True)
    tags = Column(String(255), nullable=True)  # Store as comma-separated string
    user_id = Column(String(50), index=True)
    is_favorite = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    @classmethod
    def create(
        cls,
        db: Session,
        content: str,
        user_id: str,
        title: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> "Prompt":  # noqa: PLR0913
        """Create a new prompt.

        Args:
            db: Database session
            content: The prompt content (required)
            user_id: The user ID (required)
            title: Optional title for the prompt
            category: Optional category for the prompt
            tags: Optional comma-separated tags
        """
        prompt = cls(
            title=title,
            content=content,
            category=category,
            tags=tags,
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
    def get_all_by_user(cls, db: Session, user_id: str, favorites_only: bool = False) -> list:
        """Get all prompts for a user, optionally filtered by favorites."""
        query = db.query(cls).filter(cls.user_id == user_id)
        if favorites_only:
            query = query.filter(cls.is_favorite.is_(True))
        return query.order_by(cls.title).all()

    @classmethod
    def delete(cls, db: Session, prompt_id: int) -> bool:
        """Delete a prompt."""
        prompt = cls.get_by_id(db, prompt_id)
        if prompt:
            db.delete(prompt)
            db.commit()
            return True
        return False

    @classmethod
    def toggle_favorite(cls, db: Session, prompt_id: int) -> tuple[bool, bool]:
        """Toggle the favorite status of a prompt.

        Returns:
            A tuple of (success, new_favorite_status)
        """
        prompt = cls.get_by_id(db, prompt_id)
        if prompt:
            # Toggle the favorite status using SQLAlchemy's is_ method
            new_status = not bool(prompt.is_favorite)
            prompt.is_favorite = new_status
            db.commit()
            return True, new_status
        return False, False
