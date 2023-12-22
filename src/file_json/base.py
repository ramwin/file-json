#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


"""
base class
"""


import json
import logging
from pathlib import Path

LOGGER = logging.getLogger(__name__)


class JsonData:
    """use a directory as JsonData"""
    DATA_TYPE = None

    def __init__(self, path: Path, auto_save: bool = True):
        self.path = path
        self.meta_path = self.path.joinpath(".file_json.json")
        self.meta: dict = {}
        self.post_init()
        self.auto_save = auto_save

    def post_init(self):
        """check the directory and meta info"""
        if not self.path.exists():
            LOGGER.info("create director: %s", self.path)
            self.path.mkdir(parents=True, exist_ok=True)
            with open(self.meta_path, "w", encoding="utf8") as meta_file_path:
                self.meta = self.get_meta_data()
                json.dump(
                    self.meta,
                    meta_file_path,
                )
        else:
            with open(self.meta_path, "r", encoding="utf-8") as meta_file_path:
                self.meta = json.load(meta_file_path)

    def get_meta_data(self):
        """get meta info"""
        return {
            "type": self.DATA_TYPE,
            "comment": "This file was created by python json file package, Don't edit it manually",
        }

    def save(self):
        """
        each type of JsonData should have a strategy to store the json file
        """
        raise NotImplementedError
