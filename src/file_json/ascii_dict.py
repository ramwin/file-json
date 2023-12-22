#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


"""
ascii key dict
"""


from typing import List

from .base import JsonData
from .utils import save_data


class AsciiDict(JsonData):
    """
    all data should be used to stored by as ascii key

    root_path
        - .file.json
        - key0.json.gz  # if key0 is not dict
        - key1
            key1_1.json.gz
            key1_2.json.gz
        - key2
            key2_1.json.gz
            key2_2.json.gz
        ...

    the key should only contains character that were supported by the filename
    """

    def __init__(self, *args, **kwargs):
        """
        why depth should be 2
        for a 100M size json:
            sub_dir1
                file1.json.gz
                file2.json.gz
                ...
            sub_dir2
                file17.json.gz
            ...
            sub_dir16
        each file will be 400KB, it looks good to me
        """
        self.depth = 2
        self._unsaved_data = {}
        super().__init__(*args, **kwargs)

    def save(self):
        for key, value in self._unsaved_data.items():
            for sub_key, sub_value in value.items():
                save_path = self.get_save_path(key, sub_key)
                save_data(sub_value, save_path)
        self._unsaved_data = {}

    def get_save_path(self, *keys: List[str]):
        """
        get the save path for a key
        """
        return self.path.joinpath(
            *keys).with_suffix(
                ".json.gz")
