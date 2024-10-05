# wikipy CLI

wikipy is a command line tool that is essentially a wrapper around primarily
the Wikipedia CLI with some other Wikimedia services covered. The primary purpose
of this tool was to allow me to explore the structure of the Wikipedia API for
a different project I am currently (as of October 4, 2024) working on.

The CLI is written in Python v3.12.3 and uses `typer` to handle argument parsing
and runtime type checking (supplemented with `pydantic`). `rich` is used to format
the stdout display.

Data is persisted in a SQLite database (local) using `SQLModel`.

## Features

- Search Wikipedia
- Read Wikipedia articles (HTML to Markdown)
- Get random Wikipedia articles
- Get a summary of a Wikipedia article
- Download images from Wikipedia articles
- Get the categories of a Wikipedia article
- Get the links in a Wikipedia article
- Build a graph of Wikipedia articles
    - Uses `graphviz` for images or `mermaid` for markdown
    - See [this](https://towardsdatascience.com/graph-visualisation-basics-with-python-part-iii-directed-graphs-with-graphviz-50116fb0d670) article for more information on graph visualisation
- Dataset Construction (csv)
    - Movies (this is an actual use case for me)
    - Cities

## Future Plans

- Expand to other Wikimedia [projects](https://api.wikimedia.org/wiki/Wikimedia_projects)

## Resources

- [Wikimedia API Documentation](https://api.wikimedia.org/wiki/Main_Page)
