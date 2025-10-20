@echo off
echo Starting MCP Server in Debug Mode...
echo.

REM 设置环境变量
set QDRANT_URL=http://localhost:6333
set COLLECTION_NAME=ws-77b2ac62ce00ae8e
set EMBEDDING_PROVIDER=openai_compatible
set OPENAI_API_KEY=sk-jdunbqgibzuvmglufzuluzkqxbmxtoxburabdusipasieufv
set OPENAI_BASE_URL=https://api.siliconflow.cn/v1
set EMBEDDING_MODEL=Qwen/Qwen3-Embedding-8B
set OPENAI_VECTOR_SIZE=4096
set QDRANT_SEARCH_LIMIT=20
set FASTMCP_DEBUG=true
set FASTMCP_LOG_LEVEL=DEBUG

REM 启动开发服务器
cd /d "C:\AgentProjects\mcp-qdrant-custom"
echo 浏览器将自动打开 MCP Inspector 界面...
echo.
C:\Users\Cedric\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe run fastmcp dev src/mcp_server_qdrant/server.py

pause

