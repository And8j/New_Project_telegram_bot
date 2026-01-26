from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Any

from sqlalchemy.orm import Session

from src.database.manager import DatabaseManager
from src.models.base import Base

# Create a generic type for SQLAlchemy models
ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(ABC, Generic[ModelType]):
    """
    Abstract base class for repositories, defining the main CRUD operations.
    """

    def __init__(self, model: Type[ModelType], db_manager: DatabaseManager):
        """
        Initializes the repository.

        :param model: The SQLAlchemy model class the repository will work with.
        :param db_manager: An instance of DatabaseManager for session management.
        """
        self.model = model
        self.db_manager = db_manager

    @abstractmethod
    def create(self, data: dict[str, Any]) -> ModelType:
        """Creates a new record in the database."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, model_id: int) -> ModelType | None:
        """Retrieves a record by its identifier."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """Retrieves a list of records with pagination."""
        raise NotImplementedError

    @abstractmethod
    def update(self, model_id: int, data: dict[str, Any]) -> ModelType | None:
        """Updates an existing record."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, model_id: int) -> bool:
        """Deletes a record by its identifier."""
        raise NotImplementedError
