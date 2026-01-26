from sqlalchemy.orm import relationship

from .user import User
from .category import Category
from .transaction import Expense, TransactionType

# Define relationships to avoid circular imports between model files.

# User relationships
User.categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
User.expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")

# Category relationships
Category.user = relationship("User", back_populates="categories")
Category.expenses = relationship("Expense", back_populates="category", cascade="all, delete-orphan")

# TransactionType relationships
TransactionType.expenses = relationship("Expense", back_populates="type")

# Expense relationships
Expense.user = relationship("User", back_populates="expenses")
Expense.category = relationship("Category", back_populates="expenses")
Expense.type = relationship("TransactionType", back_populates="expenses")
