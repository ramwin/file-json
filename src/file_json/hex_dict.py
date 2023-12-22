#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


"""
Hex key dict
"""


from typing import List

from hexbytes import HexBytes
from .ascii_dict import AsciiDict


class HexDict(AsciiDict):
    """
    compare to AsciiDict,
        all key will use utf8 encode to hexbytes, So the key will support any string
    """

    def get_save_path(self, *keys: List[str]):
        return self.path.joinpath(
            map(
                lambda x: HexBytes(x).hex(),
                keys
            )
        ).with_suffix("*.json.gz")
