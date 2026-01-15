"""
Wrapper server that runs mcp_server_fetch via stdio and exposes it via streamable-http
"""
from mcp.server.fastmcp import FastMCP
from langchain_mcp_adapters.client import MultiServerMCPClient

mcp = FastMCP("fetch-wrapper", host="0.0.0.0", port=8003)

# Create stdio client to connect to mcp_server_fetch
stdio_fetch_client = MultiServerMCPClient(
    {
        "fetch_mcp": {
            "command": "python",
            "args": ["-m", "mcp_server_fetch"],
            "transport": "stdio",
        }
    }
)

@mcp.tool()
async def fetch_url(url: str) -> str:
    """
    Fetch content from a URL using mcp_server_fetch.
    This is a wrapper around the fetch tool from mcp_server_fetch.
    """
    tools = await stdio_fetch_client.get_tools()
    
    fetch_tool = None
    for tool in tools:
        if "fetch" in tool.name.lower():
            fetch_tool = tool
            break
    
    if not fetch_tool:
        return "Error: Could not find fetch tool in mcp_server_fetch"
    
    try:
        result = await fetch_tool.ainvoke({"url": url})
        return result
    except Exception as e:
        return f"Error fetching {url}: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
