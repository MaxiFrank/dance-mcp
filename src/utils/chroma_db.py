"""
RAG module that combines description and steps for better retrieval
"""

import chromadb

from .moves_data import load_dance_moves


class ChromaDB:
    """
    Vector store class that allows querying of information
    """

    def __init__(self) -> None:
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(name="mcp_dance_moves")
        self.add_data_to_db()

    def get_data(self):
        "Load data from json"
        return load_dance_moves()

    def get_ids_and_docs(self):
        "Prepare ids and docs to add data to vector database"
        moves = self.get_data()
        ids = [move["id"] for move in moves]
        docs = [move["description"] + move["steps"] for move in moves]
        return ids, docs

    # TODO: No embeddings so far so results are not ideal
    # TODO: Try different models to see what works best
    def add_data_to_db(self):
        "Add data to vector database for query"
        ids, docs = self.get_ids_and_docs()
        self.collection.add(ids=ids, documents=docs)

    def query_collection(self, query_text: str, n_results=2) -> dict:
        """
        Takes in a string query_text and returns by default 2 results
        """
        results = self.collection.query(query_texts=[query_text], n_results=n_results)
        return results
