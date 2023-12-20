#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>

# pylint:disable=missing-module-docstring,missing-class-docstring,missing-function-docstring


import datetime
import logging
import tempfile

from pathlib import Path
from unittest import TestCase

from file_json.time_base_list import TimeBaseList

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
logging.getLogger("file_json").setLevel(logging.INFO)


class Test1(TestCase):

    def test(self):
        LOGGER.info("test time base list")
        with tempfile.TemporaryDirectory() as path:
            directory = Path(path, "time_base_list")
            data_list = TimeBaseList(
                key="create_datetime",
                path=directory,
            )
            data_list.append({
                "create_datetime": "2023-01-01 02:03:04",
            })
            self.assertEqual(
                data_list,
                [
                    {"create_datetime": "2023-01-01 02:03:04"},
                ]
            )
            self.assertTrue(
                directory.joinpath("2023", "01", "01.json.gz").exists()
            )
            get_data_list = TimeBaseList(
                key="create_datetime",
                path=directory,
            )
            self.assertEqual(
                get_data_list.get_meta_data()["type"],
                "time_base_list",
            )
            begin = datetime.datetime(2023, 1, 1)
            end = datetime.datetime(2023, 1, 2)
            self.assertEqual(
                get_data_list[begin],
                get_data_list[begin:end],
            )
            self.assertEqual(
                get_data_list[begin],
                [
                    {"create_datetime": "2023-01-01 02:03:04"},
                ]
            )
