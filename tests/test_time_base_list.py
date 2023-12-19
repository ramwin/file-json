#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import datetime
import tempfile

from pathlib import Path
from unittest import TestCase

from file_json.time_base_list import TimeBaseList


class Test1(TestCase):

    def test(self):
        with tempfile.TemporaryDirectory() as path:
            data_list = TimeBaseList(
                key="create_datetime",
                path=Path(path),
            )
            data_list.append({
                "create_datetime": datetime.datetime(
                    2023, 1, 1, 2, 3, 4
                )
            })
            self.assertTrue(
                Path(path, "2023", "01", "01.json.gz").exists()
            )
