"""SQL table models."""

from sqlmodel import Field, SQLModel


class Token(SQLModel, table=True):
    """Represents a persisted set of credentials."""
    id: int | None = Field(default=None, primary_key=True)
    access_token: str
    refresh_token: str
    # Unix timestamp - sqlite doesn't support datetime
    expires_at: int
