from utils.chroma_db import ChromaDB
from chromaviz import visualize_collection


def visualize_vector():
    """Visualize ChromaDB"""
    db = ChromaDB()
    visualize_collection(db.collection)

def inspect_data_in_chromadb():
    """Print IDs and Documents"""
    db = ChromaDB()
    data = db.collection.get()
    print(f"Collection: {db.collection.name}")
    print(f"IDs: {data['ids']}")
    print(f"Documents: {data['documents']}")
