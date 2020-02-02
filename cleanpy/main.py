#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import logging
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from logging import Logger
from textwrap import dedent

from .__version__ import __version__
from ._const import BUILD_CACHE_DIRS, IGNORE_DIRS, LogLevel
from ._finder import Finder
from ._manipulator import DirEntryManipulator


def parse_option() -> Namespace:
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=dedent(
            """\
            Remove cache files and temporary files that related to Python.

            Skip directories from recursive search: {}
            """.format(
                ", ".join(IGNORE_DIRS)
            )
        ),
        epilog=dedent(
            """\
            Issue tracker: https://github.com/thombashi/cleanpy/issues
            """
        ),
    )
    parser.add_argument("-V", "--version", action="version", version="%(prog)s " + __version__)

    parser.add_argument("target_dirs", metavar="DIR_PATH", nargs="+", help="positional argument")

    parser.add_argument(
        "--follow-symlinks", action="store_true", default=False, help="Follow symlinks"
    )
    parser.add_argument(
        "--include-build-cache",
        action="store_true",
        default=False,
        help="remove build cache directories: {}, docs/_build".format(", ".join(BUILD_CACHE_DIRS)),
    )
    parser.add_argument(
        "--exclude",
        metavar="PATTERN",
        help=dedent(
            """\
            a regular expression that matches files and
            directories that should be excluded on recursive searches.
            """
        ),
    )
    parser.add_argument("--dry-run", action="store_true", default=False, help="do no harm.")

    loglevel_dest = "log_level"
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-v",
        "--verbose",
        dest=loglevel_dest,
        action="store_const",
        const=logging.INFO,
        default=LogLevel.DEFAULT,
        help="shows verbose output.",
    )
    group.add_argument(
        "--debug",
        dest=loglevel_dest,
        action="store_const",
        const=logging.DEBUG,
        default=LogLevel.DEFAULT,
        help="for debug print.",
    )
    group.add_argument(
        "--quiet",
        dest=loglevel_dest,
        action="store_const",
        const=LogLevel.QUIET,
        default=LogLevel.DEFAULT,
        help="suppress execution log messages.",
    )

    return parser.parse_args()


def get_logger(log_level: int) -> Logger:
    logging.basicConfig(
        format="[%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    if log_level == LogLevel.QUIET:
        logging.disable(logging.NOTSET)

    return logger


def main():
    options = parse_option()
    logger = get_logger(options.log_level)
    manipulator = DirEntryManipulator(
        logger, follow_symlinks=options.follow_symlinks, dry_run=options.dry_run
    )
    finder = Finder(
        logger,
        manipulator=manipulator,
        exclude_pattern=options.exclude,
        include_build_cache=options.include_build_cache,
    )

    for target_dir in options.target_dirs:
        logger.debug("scan dir: {}".format(target_dir))

        try:
            for entry in finder.traverse(target_dir):
                manipulator.remove(entry)
        except (IOError, OSError) as e:
            logger.error(e)

    for entry_type, count in manipulator.remove_count.items():
        logger.info("removed {} {}".format(count, entry_type))


if __name__ == "__main__":
    main()
