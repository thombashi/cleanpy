import enum
import logging
import re
from os import DirEntry
from typing import NamedTuple, Pattern, Tuple


@enum.unique
class EntryType(enum.Enum):
    DIR = "DIR"
    FILE = "FILE"
    UNDELETABLE = "UNDELETABLE"


class RemoveTarget(NamedTuple):
    category: str
    name: str
    target_type: EntryType
    regexp: Pattern[str]


class Category:
    BUILD = "build"
    CACHE = "cache"
    ENV = "env"
    METADATA = "metadata"
    TESTING = "testing"
    ALL = [BUILD, CACHE, ENV, METADATA, TESTING]


DeleteEntry = Tuple[DirEntry, RemoveTarget]


TARGETS = (
    RemoveTarget(
        category=Category.BUILD,
        name="pyinstaller",
        target_type=EntryType.FILE,
        regexp=re.compile(
            "|".join(
                [
                    r".+\.manifest$",
                    r".+\.spec$",
                ]
            )
        ),
    ),
    RemoveTarget(
        category=Category.BUILD,
        name="Python",
        target_type=EntryType.DIR,
        regexp=re.compile(
            "|".join(
                [
                    "^build$",
                    "^dist$",
                ]
            )
        ),
    ),
    RemoveTarget(
        category=Category.CACHE,
        name="Python",
        target_type=EntryType.FILE,
        regexp=re.compile(
            "|".join(
                [
                    r".+\.py[co]$",
                ]
            )
        ),
    ),
    RemoveTarget(
        category=Category.CACHE,
        name="Python",
        target_type=EntryType.DIR,
        regexp=re.compile("|".join([r"__pycache__", r"^\.cache"])),
    ),
    RemoveTarget(
        category=Category.CACHE,
        name="pytest",
        target_type=EntryType.DIR,
        regexp=re.compile(
            "|".join(
                [
                    r"^\.pytest_cache$",
                ]
            )
        ),
    ),
    RemoveTarget(
        category=Category.CACHE,
        name="mypy",
        target_type=EntryType.DIR,
        regexp=re.compile(
            "|".join(
                [
                    r"^\.mypy_cache$",
                ]
            )
        ),
    ),
    RemoveTarget(
        category=Category.CACHE,
        name="temporary files",
        target_type=EntryType.FILE,
        regexp=re.compile(
            "|".join(
                [
                    r".+\.py\.[0-9a-z]{32}\.py$",
                ]
            )
        ),
    ),
    RemoveTarget(
        category=Category.ENV,
        name="virtual env",
        target_type=EntryType.DIR,
        regexp=re.compile("|".join([r"^\.venv$"])),
    ),
    RemoveTarget(
        category=Category.METADATA,
        name="Python",
        target_type=EntryType.DIR,
        regexp=re.compile(
            "|".join(
                [
                    r"^\.eggs",
                    r".+\.egg-info$",
                ]
            )
        ),
    ),
    RemoveTarget(
        category=Category.METADATA,
        name="pip",
        target_type=EntryType.DIR,
        regexp=re.compile("|".join([r"^pip-wheel-metadata$"])),
    ),
    RemoveTarget(
        category=Category.METADATA,
        name="type checker",
        target_type=EntryType.DIR,
        regexp=re.compile(
            "|".join(
                [
                    r"^\.pyre$",
                    r"^\.pytype$",
                ]
            )
        ),
    ),
    RemoveTarget(
        category=Category.TESTING,
        name="manager",
        target_type=EntryType.DIR,
        regexp=re.compile("|".join([r"^\.nox$", r"^\.tox$"])),
    ),
    RemoveTarget(
        category=Category.TESTING,
        name="coverage",
        target_type=EntryType.FILE,
        regexp=re.compile("|".join([r"^\.coverage$", r"^coverage\.xml$"])),
    ),
    RemoveTarget(
        category=Category.TESTING,
        name="results",
        target_type=EntryType.FILE,
        regexp=re.compile("|".join([r"^nosetests\.xml$"])),
    ),
)

SPHINX_BUILD_TARGET = RemoveTarget(
    category=Category.BUILD,
    name="sphinx",
    target_type=EntryType.DIR,
    regexp=re.compile("|".join([r"docs/_build$"])),
)

IGNORE_DIRS = (".git", ".hg", ".svn", "node_modules")
BUILD_CACHE_DIRS = ("build", "dist")


class LogLevel:
    DEFAULT = logging.WARNING
    QUIET = logging.NOTSET
