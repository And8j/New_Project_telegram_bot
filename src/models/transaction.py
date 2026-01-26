from sqlalchemy import (
    Column, Integer, Text, Numeric,
    DateTime, ForeignKey, Index, func
)
from sqlalchemy.orm import relationship

from .base import Base


class TransactionType(Base):
    """
    Represents the type of a financial transaction (e.g., expense, income).
    """
    __tablename__ = 'transaction_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)
    icon = Column(Text)

    def to_dict(self) -> dict:
        """Converts the object to a dictionary, excluding SQLAlchemy instance state."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls, data: dict) -> "TransactionType":
        """Creates a TransactionType instance from a dictionary."""
        return cls(**data)

    def __repr__(self):
        return f"<TransactionType(id={self.id}, name='{self.name}')>"


class Expense(Base):
    """
    Represents a single financial transaction (expense or income).
    """
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'))
    type_id = Column(Integer, ForeignKey('transaction_types.id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(Text, default='USD')
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('idx_expenses_created_at', created_at),
        Index('idx_expenses_user_id', user_id),
    )

    def to_dict(self) -> dict:
        """Converts the object to a dictionary, excluding SQLAlchemy instance state."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """Creates an Expense instance from a dictionary."""
        # Note: This doesn't handle relationship objects automatically.
        return cls(**data)

    def __repr__(self):
        return f"<Expense(id={self.id}, user_id={self.user_id}, amount={self.amount})>"
