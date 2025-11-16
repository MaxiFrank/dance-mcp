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
        }
    }
)
