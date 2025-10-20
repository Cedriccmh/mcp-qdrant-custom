# 测试 MCP 服务器配置
Write-Host "Testing MCP Server Configuration..." -ForegroundColor Cyan
Write-Host ""

# 设置环境变量
$env:QDRANT_URL = ":memory:"
$env:COLLECTION_NAME = "test"
$env:EMBEDDING_PROVIDER = "openai_compatible"
$env:OPENAI_API_KEY = "sk-jdunbqgibzuvmglufzuluzkqxbmxtoxburabdusipasieufv"
$env:OPENAI_BASE_URL = "https://api.siliconflow.cn/v1"
$env:EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-8B"
$env:OPENAI_VECTOR_SIZE = "4096"
$env:QDRANT_SEARCH_LIMIT = "20"
$env:FASTMCP_DEBUG = "true"
$env:FASTMCP_LOG_LEVEL = "DEBUG"

Write-Host "Environment Variables:" -ForegroundColor Yellow
Write-Host "  QDRANT_URL: $env:QDRANT_URL"
Write-Host "  COLLECTION_NAME: $env:COLLECTION_NAME"
Write-Host "  EMBEDDING_PROVIDER: $env:EMBEDDING_PROVIDER"
Write-Host "  EMBEDDING_MODEL: $env:EMBEDDING_MODEL"
Write-Host "  OPENAI_BASE_URL: $env:OPENAI_BASE_URL"
Write-Host "  OPENAI_VECTOR_SIZE: $env:OPENAI_VECTOR_SIZE"
Write-Host ""

# 切换到项目目录
Set-Location "C:\AgentProjects\mcp-qdrant-custom"

Write-Host "Starting server..." -ForegroundColor Green
Write-Host ""

# 运行服务器
& "C:\Users\Cedric\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe" run python -m mcp_server_qdrant.main

