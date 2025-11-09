"""
Data module containing utility functions such as loading data from json.
"""

import json
import os
from typing import List

DATA_DIR = "./data"


def load_dance_moves() -> List[dict]:
    """
    Load dance moves from data directory
    """
    direcotry = os.listdir(DATA_DIR)
    file_path = os.path.join(DATA_DIR, direcotry[0])
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data["moves"]
