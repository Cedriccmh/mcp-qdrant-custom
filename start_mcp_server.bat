@echo off
echo ========================================
echo Starting Qdrant MCP Server (HTTP/SSE)
echo ========================================
echo.

REM Set environment variables
REM Connect to HTTP Qdrant server instead of local storage
set QDRANT_URL=http://localhost:6333
set COLLECTION_NAME=ws-77b2ac62ce00ae8e
set EMBEDDING_PROVIDER=openai_compatible
set OPENAI_API_KEY=sk-jdunbqgibzuvmglufzuluzkqxbmxtoxburabdusipasieufv
set OPENAI_BASE_URL=https://api.siliconflow.cn/v1
set EMBEDDING_MODEL=Qwen/Qwen3-Embedding-8B
set OPENAI_VECTOR_SIZE=4096
set PYTHONUNBUFFERED=1

cd /d C:\AgentProjects\mcp-qdrant-custom

echo Server Configuration:
echo   - Transport: HTTP/SSE
echo   - Port: 8765
echo   - URL: http://localhost:8765/sse
echo   - Storage: Qdrant HTTP Server (http://localhost:6333)
echo   - Collection: ws-77b2ac62ce00ae8e
echo.
echo Starting server...
echo (Press Ctrl+C to stop)
echo.

C:\Users\Cedric\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe run python run_http_server.py

pause
