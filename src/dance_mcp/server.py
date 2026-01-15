"""
Server module that includes MCP resources and tools
"""

from typing import List, Optional

from mcp.server.fastmcp import FastMCP

from utils.moves_data import load_dance_moves
from utils.chroma_db import ChromaDB


mcp = FastMCP("pole dance", host="0.0.0.0", port=8001)
db = ChromaDB()


# TODO: Make getting dance moves data loading logic that I can use in multiple files.
@mcp.resource("mcp://pole_moves")
def load_dance_move_resource() -> List[dict]:
    """
    Load dance moves from data directory
    """
    return load_dance_moves()


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


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
