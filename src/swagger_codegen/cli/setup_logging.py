import logging

try:
    from rich.logging import RichHandler

    def setup_logging(level=logging.DEBUG):
        FORMAT = "%(message)s"
        logging.basicConfig(
            level=level, format=FORMAT, datefmt="[%X] ", handlers=[RichHandler()]
        )


except ImportError:

    def setup_logging(level=logging.DEBUG):
        logging.basicConfig(level=level)
