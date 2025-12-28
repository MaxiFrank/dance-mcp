"""
Server module that includes MCP resources and tools
"""

from typing import List, Optional

from mcp.server.fastmcp import FastMCP

from utils.moves_data import load_dance_moves
from utils.chroma_db import ChromaDB


mcp = FastMCP("pole dance")
db = ChromaDB()


# TODO: Make getting dance moves data loading logic that I can use in multiple files.
@mcp.resource("mcp://pole_moves")
def load_dance_move_resource() -> List[dict]:
    """
    Load dance moves from data directory
    """
    return load_dance_moves()


@mcp.tool()
def search_by_difficulty(difficulty: str) -> List[str]:
    """
    Get pole moves by difficulty: introductory | beginner | intermediate | advanced
    """
    relevant_moves = []
    # go through the resource
    moves = load_dance_moves()
    # find one that matches
    for move in moves:
        for key, value in move.items():
            if key == "difficulty" and value == difficulty:
                relevant_moves.append(move["id"])
    # return the list
    return relevant_moves


@mcp.tool()
def search_by_category(category: str) -> Optional[List[str]]:
    """
    Get pole moves by category: "trick | transition | floorwork | grip | spin | invert,
    """
    relevant_moves = []
    # go through the resource
    moves = load_dance_moves()
    # find one that matches
    for move in moves:
        for key, value in move.items():
            if key == "category":
                for v in value:
                    if v == category:
                        relevant_moves.append(move["id"])
    # return the list
    return relevant_moves



@mcp.tool()
def semantic_search(query: str, num: int = 3):
    """
    Get moves from user query.
    """
    response: dict = db.query_collection(query_text=query, n_results=num)
    # TODO: Typing for ids is difficult Optional[OneOrMany[ID]]
    # must return the whole response and not just the IDs, otherwise I don't have all the
    # data from the json file to make a good response here
    return str(response)


@mcp.tool()
def find_similar_moves(move: str, num: int = 3):
    """
    Find list of simiar moves given a user input of move and return by default
    3 similar moves though the num is userdefined  -> Optional[List[str]]
    """
    # TODO: Typing for ids is difficult Optional[OneOrMany[ID]]
    response = db.query_collection(
        query_text=f"give me similar \
        moves to {move}",
        n_results=num,
    )
    return response.get("ids", [])[0]


mcp.run()

