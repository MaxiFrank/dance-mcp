"""
Server module that includes MCP resources and tools
"""

import os
from typing import List, Optional

import json
from mcp.server.fastmcp import FastMCP



mcp = FastMCP("pole dance")

DATA_DIR = "./data"

# TODO: Make getting dance moves data loading logic that I can use in multiple files.
@mcp.resource("mcp://pole_moves")
def load_dance_moves() -> List[dict]:
    """
    Load dance moves from data directory
    """
    direcotry = os.listdir(DATA_DIR)
    file_path = os.path.join(DATA_DIR, direcotry[0])
    with open(file_path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data["moves"]


@mcp.tool()
def search_by_difficulty(difficulty:str) -> List[str]:
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
def search_by_category(category:str) -> Optional[List[str]]:
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
def get_prerequisites(move:str) -> Optional[List[str]]:
    """
    Get prerequisites for pole moves
    """
    # TODO: make sure I am pulling up the right prereqs
    moves = load_dance_moves()
    # find one that matches
    for m in moves:
        if m["id"] == move:
            return m["prerequisites"]
    return None
