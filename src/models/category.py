from sqlalchemy import Column, Integer, Text, ForeignKey, Index, func
from sqlalchemy.orm import relationship

from .base import Base


class Category(Base):
    """
    Represents an expense/income category belonging to a specific user.
    """
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text)

    __table_args__ = (
        Index('idx_categories_user_id_lower_name_unique', user_id, func.lower(name), unique=True),
    )

    def to_dict(self) -> dict:
        """Converts the object to a dictionary, excluding SQLAlchemy instance state."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        """Creates a Category instance from a dictionary."""
        # Note: This doesn't handle the 'user' relationship automatically.
        return cls(**data)

    def __repr__(self):
        return f"<Category(id={self.id}, user_id={self.user_id}, name='{self.name}')>"


class DefaultCategory(Base):
    """
    Represents a predefined default category that can be offered to new users.
    """
    __tablename__ = 'default_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)

    def to_dict(self) -> dict:
        """Converts the object to a dictionary, excluding SQLAlchemy instance state."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls, data: dict) -> "DefaultCategory":
        """Creates a DefaultCategory instance from a dictionary."""
        return cls(**data)

    def __repr__(self):
        return f"<DefaultCategory(id={self.id}, name='{self.name}')>"
