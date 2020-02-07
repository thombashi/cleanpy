import enum
import logging
import re
from typing import NamedTuple, Pattern


@enum.unique
class EntryType(enum.Enum):
    DIR = "DIR"
    FILE = "FILE"
    UNDELETABLE = "UNDELETABLE"


class RemoveTarget(NamedTuple):
    category: str
    name: str
    regexp: Pattern[str]


class Category:
    BUILD = "build"
    CACHE = "cache"
    ENV = "env"
    METADATA = "metadata"
    TEST = "test"
    ALL = [BUILD, CACHE, ENV, METADATA, TEST]


TARGETS = {
    EntryType.FILE: [
        RemoveTarget(
            category=Category.CACHE, name="Python", regexp=re.compile("|".join([r".+\.py[co]$",]))
        ),
        RemoveTarget(
            category=Category.BUILD,
            name="pyinstaller",
            regexp=re.compile("|".join([r".+\.manifest$", r".+\.spec$",])),
        ),
        RemoveTarget(
            category=Category.TEST,
            name="test results",
            regexp=re.compile(
                "|".join([r"^\.coverage$", r"^coverage\.xml$", r"^nosetests\.xml$",])
            ),
        ),
    ],
    EntryType.DIR: [
        RemoveTarget(
            category=Category.CACHE,
            name="Python",
            regexp=re.compile("|".join([r"__pycache__", r"^\.cache"])),
        ),
        RemoveTarget(
            category=Category.CACHE,
            name="pytest",
            regexp=re.compile("|".join([r"^\.pytest_cache$",])),
        ),
        RemoveTarget(
            category=Category.CACHE, name="mypy", regexp=re.compile("|".join([r"^\.mypy_cache$",]))
        ),
        RemoveTarget(
            category=Category.METADATA,
            name="Python",
            regexp=re.compile("|".join([r"^\.eggs", r".+\.egg-info$",])),
        ),
        RemoveTarget(
            category=Category.ENV,
            name="virtual env",
            regexp=re.compile("|".join([r"^\.nox$", r"^\.tox$", r"^\.venv$",])),
        ),
        RemoveTarget(
            category=Category.METADATA,
            name="type checker",
            regexp=re.compile("|".join([r"^\.pyre$", r"^\.pytype$",])),
        ),
    ],
}

RE_SPHINX_BUILD_DIR = re.compile("docs/_build$")

IGNORE_DIRS = (".git", ".hg", ".svn", "node_modules")
BUILD_CACHE_DIRS = ("build", "dist")


class LogLevel:
    DEFAULT = logging.WARNING
    QUIET = logging.NOTSET
