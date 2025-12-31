# dance-mcp
#### Project is deveoped following the mantra **Make it work, Make it clean, Make it efficient**
#### Significant refactor is on the horizon

### Development setup
```
# Start virtual env
poetry shell

# Install dependencies
poetry install

# Run to get access_token from spotify
poetry run python src/dance_mcp/servers/spotify/spotify_auth.py

# Run linting
poetry run task lint

# Get Spotify PKCE authentication
poetry run python src/dance_mcp/servers/spotify/spotify_auth.py

# Start FastMCP inspector for debugging
poetry run mcp dev src/dance_mcp/server.py

poetry run mcp dev src/dance_mcp/servers/spotify/spotify_server.py

# Run data scraping server
poetry run mcp dev src/dance_mcp/servers/data_scraping_server.py

# Run LangGraph
poetry run python src/agent/orchestration/main.py

```
# Start FastAPI
poetry run start

# Start Frontend in dev
npm run dev

# Run Fetch Server
npx @modelcontextprotocol/inspector uvx mcp-server-fetch


