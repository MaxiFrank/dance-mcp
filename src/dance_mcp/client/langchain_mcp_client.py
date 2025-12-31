"""
MCP multi client module
"""

# why don't I need to use src in the import path?
from langchain_mcp_adapters.client import MultiServerMCPClient


dance_client = MultiServerMCPClient(
    {
        "dance_mcp": {
            "command": "python",
            "args": ["src/dance_mcp/server.py"],
            "transport": "stdio",
        }
    }
)

spotify_client = MultiServerMCPClient(
    {
        "spotify_mcp": {
            "command": "python",
            "args": ["src/dance_mcp/servers/spotify/spotify_server.py"],
            "transport": "stdio",
        }
    }
)

fetch_mcp_client = MultiServerMCPClient(
    {
        "fetch_mcp": {
            "command": "python",
            "args": ["-m", "mcp_server_fetch"],
            "transport": "stdio",
        }
    }
)

scrape_data_client = MultiServerMCPClient(
    {
        "data_scraping_mcp": {
            "command": "python",
            "args": ["src/dance_mcp/servers/data_scraping_server.py"],
            "transport": "stdio",
        }
    }
)
