# Start MCP server with correct configuration
$env:QDRANT_URL = "http://localhost:6333"
$env:COLLECTION_NAME = "ws-fbaa5e241f1ea709"
$env:EMBEDDING_PROVIDER = "openai_compatible"
$env:OPENAI_API_KEY = "sk-jdunbqgibzuvmglufzuluzkqxbmxtoxburabdusipasieufv"
$env:OPENAI_BASE_URL = "https://api.siliconflow.cn/v1"
$env:EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-8B"
$env:OPENAI_VECTOR_SIZE = "4096"
$env:QDRANT_SEARCH_LIMIT = "20"
$env:PYTHONUNBUFFERED = "1"

Write-Host "Starting MCP server with configuration:" -ForegroundColor Green
Write-Host "  QDRANT_URL: $env:QDRANT_URL" -ForegroundColor Cyan
Write-Host "  COLLECTION_NAME: $env:COLLECTION_NAME" -ForegroundColor Cyan
Write-Host "  EMBEDDING_MODEL: $env:EMBEDDING_MODEL" -ForegroundColor Cyan
Write-Host ""

Set-Location "I:\agentic-coding-proj\qdrant-mcp-custom"
uv run python run_http_server.py

