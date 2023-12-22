#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import logging
import tempfile

from pathlib import Path
from unittest import TestCase
from file_json.ascii_dict import AsciiDict
from tests import base


LOGGER = logging.getLogger(__name__)


class Tests(TestCase):

    def test(self):
        with tempfile.TemporaryDirectory() as path:
            directory = Path(path, "ascii_dict")
            dict_data = AsciiDict(directory)
            dict_data["sub1"] = {}
            dict_data["sub2"] = [1, 2, 3]
            dict_data.save()
            LOGGER.info(list(directory.iterdir()))
            self.assertTrue(
                    directory.joinpath("sub1.json.gz").exists(),
            )
            self.assertTrue(
                    directory.joinpath("sub2.json.gz").exists(),
            )
            self.assertEqual(
                AsciiDict(directory).get_save_path("sub1"),
                directory.joinpath("sub1.json.gz"),
            )
            self.assertTrue(
                directory.joinpath("sub1.json.gz").is_file()
            )
            self.assertEqual(
                AsciiDict(directory)["sub2"],
                [1, 2, 3]
            )
