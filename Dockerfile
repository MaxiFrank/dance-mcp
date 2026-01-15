FROM python:3.12-slim
WORKDIR /app

RUN pip install poetry
COPY . /app
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Set PYTHONPATH so Python can find the src/ directory
ENV PYTHONPATH=/app
ENV BASE_DIR=/app

# Copy and make startup script executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose ports for backend and MCP servers
EXPOSE 8000 8001 8002 8003 8004

# Run the startup script that starts all MCP servers and the FastAPI app
CMD ["/start.sh"]
