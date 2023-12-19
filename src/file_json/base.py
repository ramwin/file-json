#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import json
from pathlib import Path


class JsonData:
    DATA_TYPE = None

    def __init__(self, path: Path, auto_save: True):
        self.path = path
        self.meta_path = self.path.joinpath(".file_json.json")
        self.meta: dict = {}
        self.post_init()
        self.auto_save = auto_save

    def post_init(self):
        if not self.path.exists():
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
        return {
            "type": self.DATA_TYPE,
            "comment": "This file was created by python json file package, Don't edit it manually",
        }
