import os
from typing import List
from dance_mcp.client.langchain_mcp_client import fetch_mcp_client

from mcp.server.fastmcp import FastMCP

URL_DIR = "./data/urls"
DATA_DIR = "./data/"
URLS = [
  "https://polepedia.com/level/intro/",
  "https://polepedia.com/level/beginner/",
  "https://polepedia.com/level/beginner/page/2/?el_dbe_page",
  "https://polepedia.com/level/beginner/page/3/?el_dbe_page",
  "https://polepedia.com/level/intermediate/",
  "https://polepedia.com/level/intermediate/page/2/?el_dbe_page",
  "https://polepedia.com/level/intermediate/page/3/?el_dbe_page",
  "https://polepedia.com/level/advanced/"
]

mcp = FastMCP("scrape data")

def save_tiles_file(data: str, filename: str) -> None:
    """
    Save scraped data in .md file in the ./data folder
    """
    os.makedirs(URL_DIR, exist_ok=True)
    file_path = os.path.join(URL_DIR, filename)
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(data)


@mcp.tool()
async def scrape_url(url: str):
    mcp_fetch_tool: List = await fetch_mcp_client.get_tools()
    print("mcp_fetch_tool: ", mcp_fetch_tool)
    fetch_tool = None
    # need to check this one to see what tools in mcp_fetch_tool looks like
    for tool in mcp_fetch_tool:
        if "fetch" in tool.name.lower():
            fetch_tool = tool
            break
    
    if not fetch_tool:
        return "Error: Could not find fetch tool"
    content = await fetch_tool.ainvoke({"url": url})
    save_tiles_file(content, url.split("/")[-2])

mcp.run()
