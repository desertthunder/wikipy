"""Setup the database.

NOTE it is important that the models are imported BEFORE
the database is created. This is because SQLModel will
look for the models in the same module that it is imported.
"""
from rich import print
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, create_engine

from db.models import *  # noqa: F401, F403

SQLITE_FILENAME = "db.sqlite3"

def engine(filename: str = SQLITE_FILENAME) -> Engine:
    """Create an engine for the database.

    There should only be one instance of a SQLAlchemy
    "Engine" in the entire application.
    """
    return create_engine(f"sqlite:///{filename}")


ENGINE = engine()

def create_database(verbose: bool = True, filename: str = SQLITE_FILENAME) -> None:
    """Instantiate the engine and create the database."""
    if verbose:
        print(f"Creating database at {filename}")

    # Create the database
    SQLModel.metadata.create_all(ENGINE)

    if verbose:
        print(f"Database created at {filename}")


if __name__ == "__main__":
    create_database()
