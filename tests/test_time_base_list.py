#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


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
            data_list = TimeBaseList(
                key="create_datetime",
                path=Path(path) / "time_base_list",
            )
            data_list.append({
                "create_datetime": "2023-01-01 02:03:04",
            })
            self.assertTrue(
                Path(path, "time_base_list", "2023", "01", "01.json.gz").exists()
            )
