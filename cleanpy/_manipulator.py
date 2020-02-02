import os
import shutil
from collections import defaultdict
from logging import Logger
from os import DirEntry
from typing import Dict


class DirEntryManipulator:
    def __init__(self, logger: Logger, follow_symlinks: bool, dry_run: bool):
        self.__logger = logger
        self.__follow_symlinks = follow_symlinks
        self.__dry_run = dry_run

        self.remove_count: Dict[str, int] = defaultdict(int)

        logger.debug("follow_symlinks: {}".format(follow_symlinks))
        logger.debug("dry run: {}".format(dry_run))

    def is_dir(self, entry: DirEntry) -> bool:
        return entry.is_dir(follow_symlinks=self.__follow_symlinks)

    def is_file(self, entry: DirEntry) -> bool:
        return entry.is_file(follow_symlinks=self.__follow_symlinks)

    def remove(self, entry: DirEntry) -> None:
        if self.is_dir(entry):
            self.__logger.info("remove directory: {}".format(entry.path))
            try:
                if not self.__dry_run:
                    shutil.rmtree(entry.path)
                self.remove_count["directories"] += 1
                return
            except OSError as e:
                self.__logger.error(e)

        if self.is_file(entry):
            self.__logger.info("remove file: {}".format(entry.path))
            try:
                if not self.__dry_run:
                    os.remove(entry.path)
                self.remove_count["files"] += 1
                return
            except OSError as e:
                self.__logger.error(e)

        self.__logger.error("unknown entry: {}".format(entry.path))
