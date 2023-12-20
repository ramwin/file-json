#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang <ramwin@qq.com>


"""
common utils
"""


import gzip
import json
import logging

from pathlib import Path


LOGGER = logging.getLogger(__name__)


def load_data(path: Path):
    """load json data according suffix"""
    if path.suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    if path.name.endswith(".json.gz"):
        with gzip.open(path, mode="rt", encoding="utf-8") as f:
            return json.load(f)
    raise ValueError(f"{path} not endswith .json or .json.gz")


def save_data(data, path: Path):
    """save json data according suffix"""
    path.parent.mkdir(exist_ok=True, parents=True)
    LOGGER.info("save file to: %s", path)
    if path.suffix == ".json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return
    if path.name.endswith(".json.gz"):
        with gzip.open(path, "wt") as f:

            json.dump(data, f)
        return
    raise ValueError(f"{path} not endswith .json or .json.gz")
