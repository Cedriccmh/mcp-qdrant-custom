@echo off
setlocal enabledelayedexpansion

REM ========================================
REM Configuration Section - 可在此修改配置
REM ========================================

REM Qdrant 配置
set QDRANT_URL=http://localhost:6333
REM 集合名称 - 可根据需要修改
set COLLECTION_NAME=ws-fbaa5e241f1ea709
REM Docker Qdrant 数据卷路径
set QDRANT_DATA_PATH=I:/qdrant_data

REM 嵌入模型配置
set EMBEDDING_PROVIDER=openai_compatible
set OPENAI_API_KEY=sk-jdunbqgibzuvmglufzuluzkqxbmxtoxburabdusipasieufv
set OPENAI_BASE_URL=https://api.siliconflow.cn/v1
set EMBEDDING_MODEL=Qwen/Qwen3-Embedding-8B
set OPENAI_VECTOR_SIZE=4096

REM 其他配置
set PYTHONUNBUFFERED=1

echo ========================================
echo Starting Qdrant MCP Server (HTTP/SSE)
echo ========================================
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Server Configuration:
echo   - Transport: HTTP/SSE
echo   - Port: 8765
echo   - URL: http://localhost:8765/sse
echo   - Storage: Qdrant HTTP Server (!QDRANT_URL!)
echo   - Collection: !COLLECTION_NAME!
echo   - Embedding Provider: !EMBEDDING_PROVIDER!
echo   - Embedding Model: !EMBEDDING_MODEL!
echo   - Data Volume: !QDRANT_DATA_PATH!
echo.

REM ========================================
REM MCP Server Initialization
REM ========================================
REM Check and kill any process using port 8765
echo Checking for processes using port 8765...
netstat -ano | findstr :8765 | findstr LISTENING >nul 2>&1
if !errorlevel! equ 0 (
    echo Found process using port 8765, killing it...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8765 ^| findstr LISTENING') do (
        taskkill /F /PID %%a >nul 2>&1
        echo Killed process PID: %%a
    )
    timeout /t 2 /nobreak >nul
    echo Port cleared.
) else (
    echo Port 8765 is free.
)
echo.

echo Starting server...
echo (Press Ctrl+C to stop)
echo.

uv run python run_http_server.py

pause
