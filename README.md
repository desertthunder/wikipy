# wikipy CLI

wikipy is a command line tool that is essentially a wrapper around primarily
the Wikipedia CLI with some other Wikimedia services covered. The primary purpose
of this tool was to allow me to explore the structure of the Wikipedia API for
a different project I am currently (as of October 4, 2024) working on.

The CLI is written in Python v3.12.3 and uses `typer` to handle argument parsing
and runtime type checking (supplemented with `pydantic`). `rich` is used to format
the stdout display.

Data is persisted in a SQLite database (local) using `SQLModel`.

## Usage

```bash
wikipy [OPTIONS] COMMAND [ARGS]...
```

### Commands

```plaintext
search      Search Wikipedia
read        Read Wikipedia articles
export      Export Wikipedia articles (HTML or Markdown)
random      Get random Wikipedia articles
summary     Get a summary of a Wikipedia article
download    Download images from Wikipedia articles
categories  Get the categories of a Wikipedia article
links       Get the links in a Wikipedia article
build       Build a graph or a dataset
```

## Features

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
