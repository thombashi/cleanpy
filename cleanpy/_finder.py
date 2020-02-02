import os
import re
from logging import Logger
from os import DirEntry
from typing import List, Optional, Sequence

from ._const import (
    BUILD_CACHE_DIRS,
    IGNORE_DIRS,
    RE_REMOVE_DIR,
    RE_REMOVE_FILE,
    RE_SPHINX_BUILD_DIR,
)
from ._manipulator import DirEntryManipulator


class Finder:
    def __init__(
        self,
        logger: Logger,
        manipulator: DirEntryManipulator,
        exclude_pattern: Optional[str],
        include_build_cache: bool,
    ) -> None:
        self.__logger = logger
        self.__manipulator = manipulator
        self.__include_build_cache = include_build_cache

        self.__exclude_pattern = re.compile(exclude_pattern) if exclude_pattern else None
        self.__delete_entries: List[DirEntry] = []

        logger.debug("exclude_pattern: {}".format(exclude_pattern))
        logger.debug("include_build_cache: {}".format(include_build_cache))

    def is_remove_entry(self, entry: DirEntry) -> bool:
        if self.__manipulator.is_file(entry) and RE_REMOVE_FILE.search(entry.name) is not None:
            return True

        if self.__manipulator.is_dir(entry):
            if RE_REMOVE_DIR.search(entry.name) is not None:
                return True

            if self.__include_build_cache:
                if entry.name in BUILD_CACHE_DIRS:
                    return True

                if entry.name == "_build" and RE_SPHINX_BUILD_DIR.search(entry.path) is not None:
                    return True

        return False

    def is_skip_entry(self, entry: DirEntry) -> bool:
        if self.__exclude_pattern and self.__exclude_pattern.search(entry.name):
            self.__logger.debug("match exclude pattern: {}".format(entry.path))
            return True

        if self.__manipulator.is_dir(entry) and entry.name in IGNORE_DIRS:
            return True

        return False

    def traverse(self, root: str) -> Sequence[DirEntry]:
        with os.scandir(root) as it:
            for entry in it:
                if self.is_skip_entry(entry):
                    self.__logger.debug("skip entry: {}".format(entry.path))
                    continue

                if self.is_remove_entry(entry):
                    self.__logger.debug("add delete target: {}".format(entry.path))
                    self.__delete_entries.append(entry)
                    continue

                if self.__manipulator.is_dir(entry):
                    self.traverse(entry.path)

        return self.__delete_entries
