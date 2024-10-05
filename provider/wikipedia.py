"""Wikipedia API provider.

Essentially a wrapper around the Wikipedia API.
"""

import logging
import os
import time
import typing

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel
from rich.console import Console

load_dotenv(dotenv_path=".env")


class Formatter(logging.Formatter):
    """Custom log formatter."""

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    green = "\x1b[32;20m"
    cyan = "\x1b[36;20m"
    orange = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMAT = "[%(name)s] | %(asctime)s: %(message)s" + reset

    FORMATS = {
        logging.INFO: cyan + "[INFO] | " + FORMAT,
        logging.ERROR: red + "[ERROR] | " + FORMAT,
        logging.DEBUG: green + "[DEBUG] | " + FORMAT,
        logging.WARNING: yellow + "[WARNING] | " + FORMAT,
        logging.CRITICAL: bold_red + "[CRITICAL] | " + FORMAT,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record using the custom formats."""
        fmt = self.FORMATS.get(record.levelno)

        formatter = logging.Formatter(fmt)

        return formatter.format(record)

    @classmethod
    def build_logger(
        cls: type["Formatter"], logger: logging.Logger | None = None
    ) -> logging.Logger:
        """Set the formatter for the logger."""
        if __name__ == "__main__":
            logger = logging.getLogger("wikipedia")

        if not logger:
            logger = logging.getLogger(__name__)

        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        if not logger.hasHandlers():
            stream_handler = logging.StreamHandler()

            logger.addHandler(stream_handler)

        for handler in logger.handlers:
            handler.setFormatter(cls())

        return logger


logger = Formatter.build_logger()

# Constants
client = httpx.Client()
console = Console()


class Response:
    """Semantic base class for API responses."""

    pass


# Pydantic models to validate data
class AccessTokenResponse(Response, BaseModel):
    """Access token response."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str = ""

    @property
    def expires_at(self) -> int:
        """Return the Unix timestamp for when the token expires."""
        return int(time.time()) + self.expires_in


# Provider class to collect methods
class Provider:
    """Provider base class."""

    client: httpx.Client = client


class ClientCredentials(typing.NamedTuple):
    """Client credentials."""

    client_id: str
    client_secret: str


class Wikipedia(Provider):
    """Wikipedia API wrapper/Provider class."""

    logger: logging.Logger = logger
    auth_url: str = "https://meta.wikimedia.org/w/rest.php/oauth2/access_token"

    def get_credentials(self) -> ClientCredentials:
        """Return the client credentials."""
        client_id = os.getenv("WM_CLIENT_ID")
        client_secret = os.getenv("WM_CLIENT_SECRET")

        if not client_id or not client_secret:
            raise ValueError("Client credentials not found")

        return ClientCredentials(client_id, client_secret)

    def get_access_token(self) -> AccessTokenResponse:
        """Authenticate client credentials."""
        with httpx.Client(base_url=self.auth_url) as client:
            logger.debug("Authenticating client credentials")

            resp = client.post(
                self.auth_url,
                data={
                    "grant_type": "client_credentials",
                    **self.get_credentials()._asdict(),
                },
            )

            if resp.is_error:
                logger.error(f"Error: {resp.status_code} - {resp.reason_phrase}")

            data = resp.json()

            return AccessTokenResponse(**data)
