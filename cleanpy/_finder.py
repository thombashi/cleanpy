import os
import re
from logging import Logger
from os import DirEntry
from typing import AbstractSet, Dict, List, Optional, Set, Tuple, cast

from ._const import (
    IGNORE_DIRS,
    SPHINX_BUILD_TARGET,
    TARGETS,
    Category,
    DeleteEntry,
    EntryType,
    RemoveTarget,
)
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
        self.__delete_entries: Set[DeleteEntry] = set()

        logger.debug(f"exclude_pattern: {exclude_pattern}")
        logger.debug(f"include_categories: {include_categories}")

    def is_remove_entry(self, entry: DirEntry) -> Tuple[bool, Optional[RemoveTarget]]:
        for target in self.__target_map.get(self.__manipulator.get_entry_type(entry), []):
            if target.regexp.search(entry.name):
                return (True, target)

        if Category.BUILD in self.__include_categories:
            if entry.name == "_build" and SPHINX_BUILD_TARGET.regexp.search(entry.path) is not None:
                return (True, target)

        return (False, None)

    def is_skip_entry(self, entry: DirEntry) -> bool:
        if self.__exclude_pattern and self.__exclude_pattern.search(entry.name):
            self.__logger.debug(f"match exclude pattern: {entry.path}")
            return True

        if self.__manipulator.is_dir(entry) and entry.name in IGNORE_DIRS:
            return True

        return False

    def get_delete_entries(self) -> AbstractSet[DeleteEntry]:
        return self.__delete_entries

    def traverse(self, root: str) -> AbstractSet[DeleteEntry]:
        with os.scandir(root) as it:
            for entry in it:
                if self.is_skip_entry(entry):
                    self.__logger.debug(f"skip entry: {entry.path}")
                    continue

                is_remove, remove_target = self.is_remove_entry(entry)
                if is_remove:
                    self.__logger.debug(f"add delete target: {entry.path}")
                    self.__delete_entries.add((entry, cast(RemoveTarget, remove_target)))
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
