"""Common database operations.

TODO - Refactory to the repository pattern.
"""

import logging
import typing

from sqlmodel import Session, select

from db.models import Token
from db.setup import ENGINE, Engine

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

class TokenT(typing.TypedDict):
    """A type for the kwargs passed into the Token model."""

    access_token: str
    refresh_token: str
    expires_at: int


def create_session(engine: Engine = ENGINE) -> Session:
    """Create a new session."""
    return Session(engine)


def create_token(**kwargs: typing.Unpack[TokenT]) -> Token:
    """Create a new token."""
    token = Token(**kwargs)

    with create_session() as session:
        session.add(token)
        session.commit()
        session.refresh(token)

        logger.info(f"Created token {token.id}")

    return token


def delete_all_tokens() -> None:
    """Delete all tokens."""
    with create_session() as session:
        statement = select(Token)
        tokens = session.exec(statement)

        count = 0

        for token in tokens:
            logger.info(f"Deleting token {token.id}")
            session.delete(token)

            count += 1

        session.commit()

        logger.info(f"Deleted {count} tokens")

