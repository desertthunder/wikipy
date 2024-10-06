"""Custom logging implementation."""


import logging


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
