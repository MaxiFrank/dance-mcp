#!/bin/sh

# Start all MCP servers in the background
poetry run python src/dance_mcp/server.py &
poetry run python src/dance_mcp/servers/spotify/spotify_server.py &
poetry run python src/dance_mcp/servers/data_scraping_server.py &
poetry run python src/dance_mcp/servers/fetch_server.py &

# Wait a bit for servers to start
sleep 2

# Start the main FastAPI app
poetry run start
