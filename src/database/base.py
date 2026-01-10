from sqlalchemy.orm import declarative_base

# Base class for all SQLAlchemy ORM models in the project.
# All model classes will inherit from this, so they are part of the same metadata.
Base = declarative_base()
