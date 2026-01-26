from sqlalchemy import Column, Integer, BigInteger, Text, DateTime, func
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    """
    Represents a user in the system, typically a Telegram user.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)
    full_name = Column(Text, nullable=False)
    username = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self) -> dict:
        """Converts the object to a dictionary, excluding SQLAlchemy instance state."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Creates a User instance from a dictionary."""
        return cls(**data)

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, full_name='{self.full_name}')>"
