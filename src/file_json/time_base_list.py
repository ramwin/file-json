#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


"""
time base list
"""


import datetime
import logging
from pathlib import Path

import pydash

from .base import JsonData
from .utils import load_data, save_data


LOGGER = logging.getLogger(__name__)


class TimeBaseList(JsonData):
    """
    TimeBaseList can set a key for the data.
    add data will be sorted by the datetime
    """
    DATA_TYPE = "time_base_list"

    def __init__(self, key, *args, **kwargs):
        self.key = key
        self._unsaved_data = []
        super().__init__(*args, **kwargs)

    def get_meta_data(self):
        """return meta data"""
        return {
            "type": self.DATA_TYPE,
            "key": self.key,
            "comment": "This file was created by python json file package, Don't edit it manually",
        }

    def get_datetime(self, origin_data) -> datetime.datetime:
        """
        convert data to datetime
            1. datetime.datetime object
            2. integer or float
            3. string with ISO format
        """
        if not self.key in origin_data:
            raise KeyError(f"{origin_data} does not contains {self.key}")
        data = origin_data[self.key]
        if isinstance(data, str):
            return datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        if isinstance(data, (float, int)):
            return datetime.datetime.fromtimestamp(data)
        if isinstance(data, datetime.datetime):
            return data
        raise NotImplementedError(f"{data} connot convert to datetime.datetime")

    def append(self, data):
        """append data"""
        self._unsaved_data.append(data)
        if self.auto_save:
            self.save()

    def get_path(self, data) -> Path:
        """get the save path for a data"""
        data_datetime = self.get_datetime(data)
        return self.path.joinpath(data_datetime.strftime("%Y/%m/%d.json.gz"))

    def save(self):
        """save file to file system"""
        for save_path, data in pydash.group_by(self._unsaved_data, self.get_path).items():
            if save_path.exists():
                origin_data = load_data(save_path)
            else:
                origin_data = []
            new_data = sorted(origin_data + data, key=self.get_datetime)
            save_data(new_data, save_path)
        self._unsaved_data = []

    def __getitem__(self, s):
        LOGGER.info(s)
