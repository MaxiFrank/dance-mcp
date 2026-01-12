"""
Data module containing utility functions such as loading data from json.
"""

import json
import os
from typing import List

# Use absolute path based on project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
URLS_DIR = os.path.join(BASE_DIR, "data", "urls")


def load_dance_moves() -> List[dict]:
    """
    Load dance moves from data directory
    """
    directory = os.listdir(URLS_DIR)
    data_for_db = {}
    for d in directory:
        file_path = os.path.join(URLS_DIR, d)
        with open(file_path, "r", encoding="utf-8") as file:
            data_for_db[d] = file.read()
    return data_for_db
