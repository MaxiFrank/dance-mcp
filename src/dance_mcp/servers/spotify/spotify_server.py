"""
Spotify Server module that includes MCP resources and tools
"""
import requests
from mcp.server.fastmcp import FastMCP
from dance_mcp.servers.spotify.spotify_auth import get_valid_access_token

mcp = FastMCP("spotify")

@mcp.tool()
def login():
    """
    Check login, health check
    """
    login_url = "https://api.spotify.com/v1/me"
    access_token = get_valid_access_token()
    response = requests.get(
        url=login_url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30

    )
    return response.json()

@mcp.tool()
def search_tracks_by_user_input(query, limit=3):
    """
    Search spotify using query and limit of results
    """
    access_token = get_valid_access_token()
    search_url = "https://api.spotify.com/v1/search"
    data = {
        "q": query,
        "type": "track",
        "limit": limit,
    }
    response = requests.get(
        url=search_url,
        params=data,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30

    )
    return response.json()
