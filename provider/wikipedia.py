"""Wikipedia API provider.

Essentially a wrapper around the Wikipedia API.
"""

import enum
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


# Constants
logger = Formatter.build_logger()
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


class WikipediaSearchParams(BaseModel):
    """Search endpoint params."""

    search_terms: list[str] = []
    # Can be anywhere from 1 to 100,
    #   the default is 50
    limit: int = 5

    @property
    def as_dict(self) -> dict:
        """Return the search params as a dictionary."""
        return {
            "q": "+".join(self.search_terms),
            "limit": self.limit,
        }


class WikipediaEndpoints(enum.StrEnum):
    """Available endpoints for the Wikipedia API."""

    SEARCH_PAGES = "search/page"
    SEARCH_TITLES = "search/title"

    # NOTE - Below are not yet implemented in the provider class
    # {page} is `key` in the search response item
    PAGE_WITH_HTML = "page/{page}/with_html"
    PAGE_HTML = "page/{page}/html"
    PAGE_FILES = "page/{page}/files"

    # {file} is `title` in the page files response item
    FILE = "file/{file}"


class Wikipedia(Provider):
    """Wikipedia API wrapper/Provider class."""

    logger: logging.Logger = logger
    auth_url: str = "https://meta.wikimedia.org/w/rest.php/oauth2/access_token"
    api_url: str = "https://api.wikimedia.org/core/v1/wikipedia/en/"
    random_url: str = "https://en.wikipedia.org/wiki/Special:Random"
    token: str | None = None


    @property
    def debug(self) -> bool:
        """Check the environment for the debug flag."""
        return os.getenv("DEBUG", False) in [True, "True"]

    def get_credentials(self) -> ClientCredentials:
        """Return the client credentials."""
        client_id = os.getenv("WM_CLIENT_ID")
        client_secret = os.getenv("WM_CLIENT_SECRET")

        if not client_id or not client_secret:
            raise ValueError("Client credentials not found")

        return ClientCredentials(client_id, client_secret)

    def get_access_token(self) -> httpx.Response:
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

                return resp.raise_for_status()

            return resp

    def search_titles(self, terms: list[str], limit: int = 5) -> httpx.Response:
        """Search for articles on Wikipedia."""
        params = WikipediaSearchParams(search_terms=terms, limit=limit)

        headers = {}
        if not self.token:
            logger.warning("No access token found.")
        else:
            headers = {"Authorization": f"Bearer {self.token}"}



        with httpx.Client(base_url=self.api_url) as client:
            logger.debug("Searching Wikipedia")

            resp = client.get(
                WikipediaEndpoints.SEARCH_TITLES,
                params=params.as_dict,
                headers=headers,
            )

            if resp.is_error:
                logger.error(f"Error: {resp.status_code} - {resp.reason_phrase}")

                return resp.raise_for_status()

            if self.debug:
                console.print_json(data=resp.json())

            return resp

    def search_articles(self, terms: list[str], limit: int = 2) -> httpx.Response:
        """Search for articles on Wikipedia."""
        params = WikipediaSearchParams(search_terms=terms, limit=limit)

        headers = {}
        if not self.token:
            logger.warning("No access token found.")
        else:
            headers = {"Authorization": f"Bearer {self.token}"}


        with httpx.Client(base_url=self.api_url) as client:
            logger.debug(f"Searching Wikipedia for: {",".join(terms)}")

            resp = client.get(
                WikipediaEndpoints.SEARCH_PAGES,
                params=params.as_dict,
                headers=headers,
            )

            if resp.is_error:
                logger.error(f"Error: {resp.status_code} - {resp.reason_phrase}")

                return resp.raise_for_status()

            if self.debug:
                console.print_json(data=resp.json())

            return resp

    def get_random_article(self) -> httpx.Response:
        """Get a random page from Wikipedia."""
        with httpx.Client(base_url=self.random_url) as client:
            logger.debug("Getting a random page")

            resp: httpx.Response = client.get(url="")

            if resp.is_error:
                logger.error(f"Error: {resp.status_code} - {resp.reason_phrase}")

                return resp.raise_for_status()

            logger.debug(f"Random page: {resp.headers.get("location")}")

            return resp
