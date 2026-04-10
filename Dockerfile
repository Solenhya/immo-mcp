FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies without installing the project itself
RUN uv sync --frozen --no-install-project

# Copy source code
COPY src/ ./src/

#Copy read me
COPY README.md ./

# Expose SSE port
EXPOSE 8000

# Run the MCP server
CMD ["uv", "run", "python", "-m", "src.server"]
