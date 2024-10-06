"""wikipy cli application definition."""

import enum

import typer
from rich.console import Console
from rich.style import Style
from rich.text import Text


class Tag(enum.Enum):
    """Method/Command to tag enum."""

    SEARCH = ("Search", "dodger_blue3")
    READ = ("Read", "magenta")
    EXPORT = ("Export", "yellow")
    RANDOM = ("Random", "cyan")
    SUMMARY = ("Summary", "green")
    LINKS = ("Links", "dark_violet")

    @classmethod
    def format(cls: type["Tag"], tag: str) -> str:
        """Format the tag with color."""
        return f" {tag.upper()} "


class SearchType(enum.StrEnum):
    """Search type args."""

    ARTICLES = "articles"
    TITLES = "titles"


class ExportFormat(enum.StrEnum):
    """Export format args."""

    HTML = "html"
    MARKDOWN = "markdown"
    TEXT = "text"


app = typer.Typer(name="wikipy", no_args_is_help=True)
console = Console()


@app.command(name="search", help="Search for articles on Wikipedia.")
def search_articles(
    terms: str,
    search_type: SearchType = SearchType.ARTICLES,
    limit: int = 5,
) -> None:
    """Search for articles on Wikipedia."""
    tag_text, tag_color = Tag.SEARCH.value
    tag = Text(Tag.format(tag_text), style=Style(bgcolor=tag_color))

    if search_type == "articles":
        text = Text(
            f"Searching for articles containing: '{terms}' and a limit of {limit}.",
            style=Style(color=tag_color),
        )
    else:
        text = Text(
            f"Searching for article titles containing: '{terms}'"
            "and a limit of {limit}.",
            style=Style(color=tag_color),
        )

    console.print(tag, text)


@app.command(name="read", help="Read an article from Wikipedia.")
def read_article(title: str) -> None:
    """Read an article from Wikipedia."""
    tag_text, tag_color = Tag.READ.value
    tag = Text(Tag.format(tag_text), style=Style(bgcolor=tag_color))
    text = Text(f"Reading article: {title}.", style=Style(color=tag_color))

    console.print(tag, text)


@app.command(name="export", help="Export an article from Wikipedia.")
def export_article(title: str, format: ExportFormat = ExportFormat.TEXT) -> None:
    """Export an article from Wikipedia."""
    tag_text, tag_color = Tag.EXPORT.value
    tag = Text(Tag.format(tag_text), style=Style(bgcolor=tag_color))
    text = Text(
        f"Exporting article: {title} to {format}.", style=Style(color=tag_color)
    )

    console.print(tag, text)


@app.command(name="random", help="Get a random article from Wikipedia.")
def random_article() -> None:
    """Get a random article from Wikipedia."""
    tag_text, tag_color = Tag.RANDOM.value
    tag = Text(Tag.format(tag_text), style=Style(bgcolor=tag_color))
    text = Text("Getting a random article.", style=Style(color=tag_color))

    console.print(tag, text)


@app.command(name="summary", help="Get a summary of an article from Wikipedia.")
def article_summary(title: str) -> None:
    """Get a summary of an article from Wikipedia."""
    tag_text, tag_color = Tag.SUMMARY.value
    tag = Text(Tag.format(tag_text), style=Style(bgcolor=tag_color))
    text = Text(f"Getting summary for article: {title}.", style=Style(color=tag_color))

    console.print(tag, text)


@app.command(name="links", help="Get links from an article on Wikipedia.")
def article_links(title: str) -> None:
    """Get links from an article on Wikipedia."""
    tag_text, tag_color = Tag.LINKS.value
    tag = Text(Tag.format(tag_text), style=Style(bgcolor=tag_color))
    text = Text(f"Getting links for article: {title}.", style=Style(color=tag_color))

    console.print(tag, text)


@app.command()
def main() -> None:
    """A wikipedia search CLI and reader."""
    typer.echo("Hello, wikipy!")
