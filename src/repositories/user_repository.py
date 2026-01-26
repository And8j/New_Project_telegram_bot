from typing import Any

from sqlalchemy.orm import Session

from src.database.manager import DatabaseManager
from src.models.user import User
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User model operations.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Initializes the user repository.

        :param db_manager: The database manager instance.
        """
        super().__init__(User, db_manager)

    def create_user(self, telegram_id: int, username: str | None) -> User:
        """
        Creates a new user in the database.

        :param telegram_id: The user's Telegram ID.
        :param username: The user's Telegram username.
        :return: The newly created User object.
        """
        with self.db_manager.get_session() as session:
            new_user = self.model(telegram_id=telegram_id, username=username)
            session.add(new_user)
            session.flush()
            session.refresh(new_user)
            return new_user

    def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """
        Retrieves a user by their Telegram ID.

        :param telegram_id: The user's Telegram ID.
        :return: The User object if found, otherwise None.
        """
        with self.db_manager.get_session() as session:
            return session.query(self.model).filter(self.model.telegram_id == telegram_id).first()

    def user_exists(self, telegram_id: int) -> bool:
        """
        Checks if a user with the given Telegram ID exists.

        :param telegram_id: The user's Telegram ID.
        :return: True if the user exists, False otherwise.
        """
        with self.db_manager.get_session() as session:
            return session.query(self.model.id).filter(self.model.telegram_id == telegram_id).first() is not None

    def update_username(self, telegram_id: int, new_username: str | None) -> User | None:
        """
        Updates the username for a user with the given Telegram ID.

        :param telegram_id: The user's Telegram ID.
        :param new_username: The new username to set.
        :return: The updated User object if found, otherwise None.
        """
        with self.db_manager.get_session() as session:
            user = self.get_by_telegram_id(telegram_id)
            if user:
                user.username = new_username
                session.add(user)
                session.flush()
                session.refresh(user)
                return user
            return None

    # Note: The abstract methods from BaseRepository (create, get_by_id, etc.)
    # are not implemented as they are not required by the current request.
    # They would need to be implemented if UserRepository was to be used polymorphically.
