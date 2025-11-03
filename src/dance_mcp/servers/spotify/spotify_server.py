"""
Spotify Server module that includes MCP resources and tools
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("spotify")

@mcp.tool
def search_spotify():
    """
    Search spotify using query and limit of results
    """
    # TODO: implement function

