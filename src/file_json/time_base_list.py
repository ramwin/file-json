#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


"""
time base list
"""


import datetime
import logging
from pathlib import Path
from typing import Union, Literal

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
        return self.get_datetime_path(data_datetime)

    def get_datetime_path(self, datetime_obj: Union[datetime.date, datetime.datetime]) -> Path:
        """
        get the json file path according the datetime
        """
        return self.path.joinpath(
                datetime_obj.strftime("%Y/%m/%d.json.gz"))

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
        # pylint: disable=too-many-branches
        if isinstance(s, (datetime.date, datetime.datetime)):
            path = self.get_datetime_path(s)
            if path.exists():
                return load_data(path)
            return []

        results = []
        for year_dir in sorted(self.path.iterdir()):
            if year_dir.name == ".file_json.json":
                continue
            year_contain = self.contain_slice(
                self.get_potential_slice(int(year_dir.name)),
                s,
            )
            if year_contain == "none":
                continue
            for month_dir in sorted(year_dir.iterdir()):
                if year_contain == "all":
                    month_contain = "all"
                else:
                    month_contain = self.contain_slice(
                        self.get_potential_slice(
                            year=int(year_dir.name),
                            month=int(month_dir.name),
                        ),
                        s,
                    )
                if month_contain == "none":
                    continue
                for day_file in sorted(month_dir.iterdir()):
                    if month_contain == "all":
                        day_contain = "all"
                    else:
                        day_contain = self.contain_slice(
                                self.get_potential_slice(
                                    year=int(year_dir.name),
                                    month=int(month_dir.name),
                                    day=int(day_file.name.split(".")[0]),
                                ),
                                s,
                        )
                    if day_contain == "none":
                        continue
                    day_data = load_data(day_file)
                    if day_contain == "all":
                        results.extend(day_data)
                    else:
                        results.extend(pydash.filter_(
                            day_data,
                            lambda x: self.check_in(self.get_datetime(x), s)
                        ))
        return results

    @staticmethod
    def check_in(datetime_obj, target_slice):
        """
        check if datetime_obj in [start: end]
            start included
            end not included
        """
        if datetime_obj >= target_slice.stop:
            return False
        if target_slice.start:
            if datetime_obj < target_slice.start:
                return False
        return True

    @staticmethod
    def contain_slice(data_slice: slice, target_slice: slice) -> Literal["all", "none", "both"]:
        """
        check if a data_slice may contain target_slice
            all: all data were in slice
            none: none data were in slice
            both: some data may be in slice
        """
        if target_slice.start is None:
            if target_slice.stop > data_slice.stop:
                return "all"
            if target_slice.stop < data_slice.start:
                return "none"
            return "both"
        if target_slice.start > data_slice.stop:
            return "none"
        if target_slice.stop < data_slice.start:
            return "none"
        return "both"

    @staticmethod
    def get_potential_slice(year: int, month: int=None, day: int=None) -> slice:
        """
        guess the data slice from year month day
        e.g
            year=2023 may contains data from 2023-01-01:00:00:00 to 2024-01-01 00:00:00
        return
            slice(datetime.datetime, datetime.datetime)
        """
        if month is None and day is None:
            return slice(
                datetime.datetime(year, 1, 1),
                datetime.datetime(year+1, 1, 1)
            )
        if day is None:
            if month == 12:
                return slice(
                    datetime.datetime(year, month, 1),
                    datetime.datetime(year+1, 1, 1))
            return slice(
                datetime.datetime(year, month, 1),
                datetime.datetime(year, month+1, 1))
        begin = datetime.datetime(year, month, day)
        return slice(begin, begin + datetime.timedelta(days=1))

    def __iter__(self):
        self.save()
        for json_file in sorted(self.path.rglob("*.json.gz")):
            for item in load_data(json_file):
                yield item
