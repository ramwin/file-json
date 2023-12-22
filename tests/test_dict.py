#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


import tempfile
from pathlib import Path
from unittest import TestCase
from file_json.ascii_dict import AsciiDict
from tests import base


class Tests(TestCase):

    def test(self):
        with tempfile.TemporaryDirectory() as path:
            directory = Path(path, "ascii_dict")
            dict_data = AsciiDict(directory)
            dict_data["sub1"] = {}
            dict_data["sub2"] = [1, 2, 3]
            dict_data.save()
