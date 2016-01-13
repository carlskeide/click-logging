import sys
import logging
from contextlib import contextmanager
from collections import namedTuple

import click

__all__ = ["ClickLoggingHandler",
           "ClickLoggingFormatter",
           "progressbar",
           "basicConfig"]

_format = namedTuple("log_format", ("prefix", "style"))

LEVEL_FORMATS = {
    "CRITICAL": _format("[c]", {"fg": "red", "bold": True, "blink": True}),
    "ERROR": _format("[e]", {"fg": "red", "bold": True, "blink": True}),
    "WARNING": _format("[w]", {"fg": "yellow", "bold": True}),
    "INFO": _format("[i]", {"fg": "green", "bold": True}),
    "DEBUG": _format("[d]", {"fg": "white", "bold": False})
}


class ClickLoggingHandler(logging.Handler, object):
    def emit(self, record):
        message = self.format(record)
        click.echo(message, sys.stderr)


class ClickLoggingFormatter(logging.Formatter, object):
    def __init__(self, *args, **kwargs):
        self.style = kwargs.pop("style", True)
        super(ClickLoggingFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        formatted_string = super(ClickLoggingFormatter, self).format(record)

        try:
            level_format = LEVEL_FORMATS[record.levelname]
            level_prefix = level_format.prefix

        except KeyError:
            #: Unknown levels aren't formatted, but still emitted.
            pass

        else:
            if self.style:
                level_prefix = click.style(level_prefix, **level_format.style)

            formatted_string = "{} {}".format(level_prefix, formatted_string)

        finally:
            return formatted_string


@contextmanager
def progressbar(iterator, verbosity, length=None):
    """ Display an ASCII progressbar for the supplied iterator, if appropriate.

    :param iterator: Any iterable object.
    :type iterator: iterable
    :param verbosity: The current logging level.
    :type verbosity: int
    :param length: The length of the supplied iterable,
    required if the object doesn't provide len()
    :type length: int

    :return: An enriched version of the supplied iterable.
    """

    if verbosity == logging.INFO:
        if not length:
            length = len(iterator)

        with click.progressbar(iterator, length=length) as _iterator:
            yield _iterator
    else:
        yield iterator


def _basic_config(level=logging.INFO):
    """ Initialize and return a boilerplate logging environment for click.

    :param log_level: Initial log level for the root logging handler.
    :type log_level: int
    """

    root_logger = logging.getLogger("")
    root_logger.setLevel(level)

    click_log_handler = ClickLoggingHandler()
    click_log_formatter = ClickLoggingFormatter(style=True)
    click_log_handler.setFormatter(click_log_formatter)

    root_logger.addHandler(click_log_handler)


# PEP8 compatibility kludge
basicConfig = _basic_config
