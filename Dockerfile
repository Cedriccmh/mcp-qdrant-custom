FROM python:3.11-slim

WORKDIR /app

# Install uv for package management
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src ./src
COPY run_http_server.py ./

# Install dependencies
RUN uv sync --frozen

# Expose the default port for SSE transport (matches settings.py default)
EXPOSE 8765

# Set environment variables with defaults that can be overridden at runtime
ENV QDRANT_URL=""
ENV QDRANT_API_KEY=""
ENV COLLECTION_NAME="your-collection-name"
ENV EMBEDDING_PROVIDER="fastembed"
ENV EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"
ENV PORT="8765"
ENV PYTHONUNBUFFERED="1"

# Run the server with SSE transport using the local code
CMD ["uv", "run", "python", "run_http_server.py"]
