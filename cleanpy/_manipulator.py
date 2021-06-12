import os
import shutil
from collections import defaultdict
from logging import Logger
from os import DirEntry
from typing import Dict

from ._const import EntryType, RemoveTarget


class DirEntryManipulator:
    def __init__(self, logger: Logger, force: bool, follow_symlinks: bool, dry_run: bool):
        self.__logger = logger
        self.__force = force
        self.__follow_symlinks = follow_symlinks
        self.__dry_run = dry_run

        self.remove_count: Dict[str, int] = defaultdict(int)
        self.error_count: Dict[str, int] = defaultdict(int)

        logger.debug(f"follow_symlinks: {follow_symlinks}")
        logger.debug(f"dry run: {dry_run}")

    def is_dir(self, entry: DirEntry) -> bool:
        return entry.is_dir(follow_symlinks=self.__follow_symlinks)

    def is_file(self, entry: DirEntry) -> bool:
        return entry.is_file(follow_symlinks=self.__follow_symlinks)

    def get_entry_type(self, entry: DirEntry) -> EntryType:
        if self.is_dir(entry):
            return EntryType.DIR

        if self.is_file(entry):
            return EntryType.FILE

        return EntryType.UNDELETABLE

    def remove(self, entry: DirEntry, remove_target: RemoveTarget) -> None:
        if not self.__prompt_remove(entry.path):
            self.__logger.warning(f"skip removal of '{entry.path}'")
            return

        if self.is_dir(entry):
            self.__logger.info(
                f"remove directory [{remove_target.category} - {remove_target.name}]: {entry.path}"
            )
            try:
                if not self.__dry_run:
                    shutil.rmtree(entry.path)
                self.remove_count["directories"] += 1
            except OSError as e:
                self.__logger.error(f"failed to remove a directory '{entry.path}': {e}")
                self.error_count["directories"] += 1
            return

        if self.is_file(entry):
            self.__logger.info(
                f"remove file [{remove_target.category} - {remove_target.name}]: {entry.path}"
            )
            try:
                if not self.__dry_run:
                    os.remove(entry.path)
                self.remove_count["files"] += 1
                return
            except OSError as e:
                self.__logger.error(f"failed to remove a file '{entry.path}': {e}")
                self.error_count["files"] += 1

            return

        self.__logger.error(f"unknown entry: {entry.path}")

    def __prompt_remove(self, remove_path: str) -> bool:
        if self.__force:
            return True

        response = input(f"Remove '{remove_path}'? [y/N]: ")
        response = response.strip().casefold()

        if not response:
            return False

        if response[0] == "y":
            return True

        return False
