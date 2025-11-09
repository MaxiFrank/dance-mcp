# dance-mcp

### Development setup
```
# Start virtual env
poetry shell

# Install dependencies
poetry install

# Run to get access_token from spotify
poetry run mcp dev src/dance_mcp/servers/spotify/spotify_server.py

# Run linting
poetry run task lint

# Start FastMCP inspector for debugging
poetry run mcp dev src/dance_mcp/server.py

poetry run mcp dev src/dance_mcp/servers/spotify/spotify_server.py

# Run LangGraph
poetry run python src/agent/orchestration/main.py

```

