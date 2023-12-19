#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import datetime
import pydash

from .base import JsonData


class TimeBaseList(JsonData):
    DATA_TYPE = "time_base_list"

    def __init__(self, key, *args, **kwargs):
        self.key = key
        self._unsaved_data = []
        super().__init__(*args, **kwargs)

    def get_meta_data(self):
        return {
            "type": self.DATA_TYPE,
            "key": self.key,
            "comment": "This file was created by python json file package, Don't edit it manually",
        }

    @staticmethod
    def get_datetime(data) -> datetime.datetime:
        if isinstance(data, str):
            return datetime.datetime.strptime(data[self.key], "%Y-%m-%d %H:%M:%S")
        if isinstance(data, (float, int)):
            return datetime.datetime.fromtimestamp(data)
        if isinstance(data, datetime.datetime):
            return data

    def append(self, data):
        data_datetime = self.get_datetime(data[self.key])
        self._unsaved_data.append(data)
        if self.auto_save:
            self.save()

    def get_path(self, data) -> Path:
        date_datetime = self.get_datetime(data[self.key])
        return data_datetime.strftime("%Y/%m/%d.json.gz")

    def save(self):
        raise NotImplementedError
