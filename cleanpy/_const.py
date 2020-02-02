import logging
import re


RE_REMOVE_FILE = re.compile(
    "|".join(
        [
            r"^\.coverage$",
            r"^coverage\.xml$",
            r"^nosetests\.xml$",
            r".+\.manifest$",
            r".+\.spec$",
            r".+\.py[co]$",
        ]
    )
)
RE_REMOVE_DIR = re.compile(
    "|".join(
        [
            r"__pycache__",
            r"^\.cache",
            r"^\.eggs",
            r"^\.mypy_cache$",
            r"^\.nox$",
            r"^\.pyre$",
            r"^\.pytest_cache$",
            r"^\.pytype$",
            r"^\.tox$",
            r"^\.venv$",
            r".+\.egg-info$",
        ]
    )
)
RE_SPHINX_BUILD_DIR = re.compile("docs/_build$")

IGNORE_DIRS = (".git", ".hg", ".svn", "node_modules")
BUILD_CACHE_DIRS = ("build", "dist")


class LogLevel:
    DEFAULT = logging.WARNING
    QUIET = logging.NOTSET
