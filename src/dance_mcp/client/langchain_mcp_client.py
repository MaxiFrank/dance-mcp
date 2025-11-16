"""
MCP multi client module
"""

# why don't I need to use src in the import path?
from langchain_mcp_adapters.client import MultiServerMCPClient


client = MultiServerMCPClient(
    {
        "dance_mcp": {
            "command": "python",
            "args": ["src/dance_mcp/server.py"],
            "transport": "stdio",
        },
        "spotify_mcp": {
            "command": "python",
            "args": ["src/dance_mcp/servers/spotify/spotify_server.py"],
            "transport": "stdio",
        },
    }
)
