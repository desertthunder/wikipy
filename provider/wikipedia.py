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

from libs.logger import Formatter

load_dotenv(dotenv_path=".env")

logger = Formatter.build_logger()
client = httpx.Client()
console = Console()


class Response(BaseModel):
    """Semantic base class for API responses."""

    pass


class Params(BaseModel):
    """Base class for API params."""

    pass


class Provider:
    """Provider base class."""

    client: httpx.Client = client


class AccessTokenResponse(Response):
    """Access token response."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str = ""

    @property
    def expires_at(self) -> int:
        """Return the Unix timestamp for when the token expires."""
        return int(time.time()) + self.expires_in


class ClientCredentials(typing.NamedTuple):
    """Client credentials."""

    client_id: str
    client_secret: str


class WikipediaSearchParams(Params):
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

    def load_credentials(self) -> ClientCredentials:
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
                    **self.load_credentials()._asdict(),
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
