#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


"""
ascii key dict
"""


from .base import JsonData
from .utils import load_data, save_data


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
        with a 100M size json, 16key, each key contains 16key. then the file size would be 400kb. which is suitable.
        """
        self.depth = 2
        self._unsaved_data = {}
        super().__init__(*args, **kwargs)

    def save(self):
        for key, value in self._unsaved_data.items():
            for sub_key, sub_value in value.items():
                save_path = self.path.joinpath(key, sub_key).with_suffix(".json.gz")
                save_data(sub_value, save_path)
        self._unsaved_data = {}
