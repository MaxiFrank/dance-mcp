# dance-mcp

### Development setup
```
# Start virtual env
poetry shell

# Install dependencies
poetry install

# Run linting
poetry run task lint

# Start FastMCP inspector for debugging
poetry run mcp dev src/dance_mcp/server.py

poetry run mcp dev src/dance_mcp/servers/spotify/server.py

```

