import datetime
from typing import Any

from sqlalchemy import extract
from sqlalchemy.orm import Session

from src.database.manager import DatabaseManager
from src.models.transaction import Expense
from src.repositories.base import BaseRepository


class TransactionRepository(BaseRepository[Expense]):
    """
    Repository for Expense (Transaction) model operations.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Initializes the transaction repository.

        :param db_manager: The database manager instance.
        """
        super().__init__(Expense, db_manager)

    def create_transaction(
        self,
        user_id: int,
        category_id: int,
        amount: float,
        transaction_date: datetime.date,
        notes: str | None = None,
    ) -> Expense:
        """
        Creates a new expense transaction.

        :param user_id: The ID of the user performing the transaction.
        :param category_id: The ID of the transaction category.
        :param amount: The transaction amount.
        :param transaction_date: The date of the transaction.
        :param notes: Optional notes for the transaction.
        :return: The newly created Expense object.
        """
        with self.db_manager.get_session() as session:
            new_expense = self.model(
                user_id=user_id,
                category_id=category_id,
                amount=amount,
                transaction_date=transaction_date,
                notes=notes,
            )
            session.add(new_expense)
            session.flush()
            session.refresh(new_expense)
            return new_expense

    def get_user_transactions(self, user_id: int) -> list[Expense]:
        """
        Retrieves all transactions for a specific user.

        :param user_id: The user's ID.
        :return: A list of Expense objects.
        """
        with self.db_manager.get_session() as session:
            return session.query(self.model).filter(self.model.user_id == user_id).all()

    def get_paginated_transactions(self, user_id: int, skip: int = 0, limit: int = 10) -> list[Expense]:
        """
        Retrieves transactions for a user with pagination.

        :param user_id: The user's ID.
        :param skip: The number of records to skip.
        :param limit: The maximum number of records to return.
        :return: A list of Expense objects.
        """
        with self.db_manager.get_session() as session:
            return session.query(self.model).filter(self.model.user_id == user_id).offset(skip).limit(limit).all()

    def update_transaction(self, transaction_id: int, data: dict[str, Any]) -> Expense | None:
        """
        Updates a transaction by its ID.

        :param transaction_id: The ID of the transaction to update.
        :param data: A dictionary with the fields to update.
        :return: The updated Expense object or None if not found.
        """
        with self.db_manager.get_session() as session:
            transaction = session.query(self.model).filter(self.model.id == transaction_id).first()
            if transaction:
                for key, value in data.items():
                    setattr(transaction, key, value)
                session.add(transaction)
                session.flush()
                session.refresh(transaction)
                return transaction
            return None

    def delete_transaction(self, transaction_id: int) -> bool:
        """
        Deletes a transaction by its ID.

        :param transaction_id: The ID of the transaction to delete.
        :return: True if deletion was successful, False otherwise.
        """
        with self.db_manager.get_session() as session:
            transaction = session.query(self.model).filter(self.model.id == transaction_id).first()
            if transaction:
                session.delete(transaction)
                return True
            return False

    def get_monthly_transactions(self, user_id: int, year: int, month: int) -> list[Expense]:
        """
        Retrieves all transactions for a user for a specific month and year.

        :param user_id: The user's ID.
        :param year: The year.
        :param month: The month.
        :return: A list of Expense objects for the specified period.
        """
        with self.db_manager.get_session() as session:
            return (
                session.query(self.model)
                .filter(
                    self.model.user_id == user_id,
                    extract("year", self.model.transaction_date) == year,
                    extract("month", self.model.transaction_date) == month,
                )
                .all()
            )

    # Note: The abstract methods from BaseRepository (create, get_by_id, etc.)
    # are not implemented as they are not required by the current request.
