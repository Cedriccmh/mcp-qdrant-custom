@echo off
setlocal enabledelayedexpansion

REM ========================================
REM Configuration Section
REM ========================================
REM Configuration is now loaded from .env file
REM Please edit .env file to change settings

REM Set Python unbuffered output
set PYTHONUNBUFFERED=1

echo ========================================
echo Starting Qdrant MCP Server (HTTP/SSE)
echo ========================================
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo Configuration loaded from .env file
echo Please check .env file for current settings
echo.
echo Starting server...
echo.

REM ========================================
REM MCP Server Initialization
REM ========================================
REM Note: Port is configured in .env file (default: 8765)
REM Kill any process using port 8765 (single attempt)
echo Checking port 8765...
netstat -ano | findstr :8765 | findstr LISTENING >nul 2>&1
if !errorlevel! equ 0 (
    echo Port 8765 in use, attempting to free it...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8765 ^| findstr LISTENING') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
) else (
    echo Port 8765 is free.
)
echo.

echo Starting server...
echo (Press Ctrl+C to stop)
echo.

uv run python run_http_server.py

pause
