"""
RAG module that combines description and steps for better retrieval
"""

import json
import os
from typing import List

import chromadb

DATA_DIR = "./data"

# TODO: Make getting dance moves data loading logic that I can use in multiple files.
def load_dance_moves() -> List[dict]:
    """
    Load dance moves from data directory
    """
    direcotry = os.listdir(DATA_DIR)
    file_path = os.path.join(DATA_DIR, direcotry[0])
    with open(file_path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data["moves"]


chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="mcp_dance_moves")

moves = load_dance_moves()

ids = [move["id"] for move in moves]
docs = [move["description"] + move["steps"] for move in moves]

for move in moves:
    collection.add(
        ids=ids,
        documents=docs
    )

# No embeddings right now
results = collection.query(
    query_texts=["I want easy graceful spins with tricks, \
    moves within trick category only except spin"], # Chroma will embed this for you
    n_results=2 # how many results to return
)
print(results)
