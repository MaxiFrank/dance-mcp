"""
MCP multi client module
"""

# why don't I need to use src in the import path?
from langchain_mcp_adapters.client import MultiServerMCPClient


dance_client = MultiServerMCPClient(
    {
        "dance_mcp": {
            "url": "http://localhost:8001/mcp",
            "transport": "streamable_http",
        }
    }
)

spotify_client = MultiServerMCPClient(
    {
        "spotify_mcp": {
            "url": "http://localhost:8004/mcp",
            "transport": "streamable_http",
        }
    }
)

fetch_mcp_client = MultiServerMCPClient(
    {
        "fetch_mcp": {
            "url": "http://localhost:8003/mcp",
            "transport": "streamable_http",
        }
    }
)

scrape_data_client = MultiServerMCPClient(
    {
        "data_scraping_mcp": {
            "url": "http://localhost:8002/mcp",
            "transport": "streamable_http",
        }
    }
)
