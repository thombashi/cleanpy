import os
import re
from logging import Logger
from os import DirEntry
from typing import AbstractSet, Dict, List, Optional, Set

from ._const import IGNORE_DIRS, RE_SPHINX_BUILD_DIR, TARGETS, Category, EntryType, RemoveTarget
from ._manipulator import DirEntryManipulator


class Finder:
    def __init__(
        self,
        logger: Logger,
        manipulator: DirEntryManipulator,
        exclude_pattern: Optional[str],
        include_categories: AbstractSet[str],
    ) -> None:
        self.__logger = logger
        self.__manipulator = manipulator
        self.__include_categories = include_categories

        self.__target_map = self.__make_target_map()
        self.__exclude_pattern = re.compile(exclude_pattern) if exclude_pattern else None
        self.__delete_entries: Set[DirEntry] = set([])

        logger.debug(f"exclude_pattern: {exclude_pattern}")
        logger.debug(f"include_categories: {include_categories}")

    def __is_remove_category(self, category: str) -> bool:
        return category in self.__include_categories

    def is_remove_entry(self, entry: DirEntry) -> bool:
        for target in self.__target_map.get(self.__manipulator.get_entry_type(entry), []):
            if target.regexp.search(entry.name):
                return True

        if Category.BUILD in self.__include_categories:
            if entry.name == "_build" and RE_SPHINX_BUILD_DIR.search(entry.path) is not None:
                return True

        return False

    def is_skip_entry(self, entry: DirEntry) -> bool:
        if self.__exclude_pattern and self.__exclude_pattern.search(entry.name):
            self.__logger.debug(f"match exclude pattern: {entry.path}")
            return True

        if self.__manipulator.is_dir(entry) and entry.name in IGNORE_DIRS:
            return True

        return False

    def get_delete_entries(self) -> AbstractSet[DirEntry]:
        return self.__delete_entries

    def traverse(self, root: str) -> AbstractSet[DirEntry]:
        with os.scandir(root) as it:
            for entry in it:
                if self.is_skip_entry(entry):
                    self.__logger.debug(f"skip entry: {entry.path}")
                    continue

                if self.is_remove_entry(entry):
                    self.__logger.debug(f"add delete target: {entry.path}")
                    self.__delete_entries.add(entry)
                    continue

                if self.__manipulator.is_dir(entry):
                    self.traverse(entry.path)

        return self.__delete_entries

    def __make_target_map(self) -> Dict[EntryType, List[RemoveTarget]]:
        target_map: Dict[EntryType, List[RemoveTarget]] = {}

        for target in TARGETS:
            if target.category not in self.__include_categories:
                continue

            target_map.setdefault(target.target_type, []).append(target)

        return target_map
