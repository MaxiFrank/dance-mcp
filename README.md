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

To Test the Streamable Http is working
poetry run python src/dance_mcp/servers/data_scraping_server.py 
poetry run python src/dance_mcp/servers/fetch_server.py
poetry run mcp dev src/dance_mcp/servers/data_scraping_server.py 
poetry run mcp dev src/dance_mcp/servers/spotify/spotify_server.py

Next:
spotify server, make sure it's streamable.

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

# Build dance server image in Docker
 docker build -t dance-mcp .

# Start dance server container
 docker run dance-mcp

# Build dance client image in Docker
docker build -t dance .

# Start dance client container
 docker run dance

# Docker commands
    docker ps: inspect containers
    docker images or docker image ls: inspect images
    docker rmi -f image name or id: force remove an image

# docker-compose using .yml file in root directory
docker-compose -f docker-compose-dev.yml up --build


# Make changes to container in ./src or ./dance folders
docker-compose -f docker-compose-dev.yml restart [SERVICE...]
