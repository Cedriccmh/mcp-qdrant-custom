# mcp-server-qdrant (Enhanced Version)

**基于 FastMCP 的 Qdrant 向量数据库 MCP 服务器** | *Qdrant Vector Database MCP Server based on FastMCP*

[![smithery badge](https://smithery.ai/badge/mcp-server-qdrant)](https://smithery.ai/protocol/mcp-server-qdrant)

---

## 📖 概述 | Overview

**中文：** 这是一个增强版的 [Qdrant](https://qdrant.tech/) MCP (Model Context Protocol) 服务器，为 LLM 应用提供语义记忆存储和检索能力。

**English:** An enhanced [Qdrant](https://qdrant.tech/) MCP (Model Context Protocol) server that provides semantic memory storage and retrieval for LLM applications.

### ✨ 增强特性 | Enhanced Features

- 🎯 **相似度阈值过滤** | Score threshold filtering for better result quality
- 📝 **完善的配置文档** | Comprehensive configuration documentation
- 🐳 **优化的 Docker 支持** | Improved Docker support
- 🔧 **灵活的嵌入模型** | Flexible embedding provider support (FastEmbed / OpenAI-compatible)
- 📊 **完整的测试套件** | Complete test suite in `tests/` directory

---

## 🚀 快速开始 | Quick Start

### 1️⃣ 安装 | Installation

```bash
# 或从源码安装 | Or install from source
git clone <repository-url>
cd mcp-qdrant-custom
```

### 2️⃣ 配置 | Configuration

**复制配置模板** | *Copy configuration template:*

```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

**编辑 `.env` 文件** | *Edit `.env` file:*

```env
# Qdrant 连接 | Qdrant Connection
QDRANT_URL=http://localhost:6333
COLLECTION_NAME=your-collection

# 嵌入模型 | Embedding Model
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=Qwen/Qwen3-Embedding-8B
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
OPENAI_VECTOR_SIZE=4096

# 可选：相似度阈值 | Optional: Score Threshold
QDRANT_SCORE_THRESHOLD=0.5
```

📚 **详细配置指南** | *Detailed configuration:* 查看 | See [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md)

### 3️⃣ 运行服务器 | Run Server

```bash
# Windows
start_mcp_server.bat

# Python 直接运行 | Run with Python
uv run python run_http_server.py

# 或开发模式 | Or development mode
COLLECTION_NAME=test fastmcp dev src/mcp_server_qdrant/server.py
```

### 4️⃣ 使用 Docker | Using Docker

```bash
# 构建镜像 | Build image
docker build -t mcp-server-qdrant .

# 运行容器 (FastEmbed) | Run with FastEmbed
docker run -p 8765:8765 \
  -e QDRANT_URL=http://your-qdrant:6333 \
  -e COLLECTION_NAME=your-collection \
  mcp-server-qdrant

# 使用 OpenAI 兼容嵌入 | With OpenAI-compatible embeddings
docker run -p 8765:8765 \
  -e QDRANT_URL=http://your-qdrant:6333 \
  -e COLLECTION_NAME=your-collection \
  -e EMBEDDING_PROVIDER=openai_compatible \
  -e EMBEDDING_MODEL=text-embedding-3-small \
  -e OPENAI_API_KEY=your-api-key \
  -e OPENAI_VECTOR_SIZE=1536 \
  mcp-server-qdrant
```

🐳 **Docker 故障排除** | *Docker troubleshooting:* [`docs/DOCKER_TROUBLESHOOTING.md`](docs/DOCKER_TROUBLESHOOTING.md)

---

## 🛠️ 核心功能 | Core Features

### MCP 工具 | MCP Tools

#### 1. `qdrant-store`
**存储信息到 Qdrant** | *Store information in Qdrant*

```json
{
  "information": "描述或内容 | Description or content",
  "metadata": {"key": "value"},
  "collection_name": "可选 | Optional (if default set)"
}
```

#### 2. `qdrant-find`
**语义搜索相关信息** | *Semantic search for relevant information*

```json
{
  "query": "搜索查询 | Search query",
  "collection_name": "可选 | Optional (if default set)"
}
```

---

## ⚙️ 环境变量 | Environment Variables

### 核心配置 | Core Settings

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `QDRANT_URL` | Qdrant 服务器 URL | 无 |
| `QDRANT_API_KEY` | Qdrant API 密钥 | 无 |
| `COLLECTION_NAME` | 默认集合名称 | 无 |
| `QDRANT_LOCAL_PATH` | 本地 Qdrant 路径 | 无 |

### 搜索配置 | Search Settings

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `QDRANT_SEARCH_LIMIT` | 最大结果数 | `10` |
| `QDRANT_SCORE_THRESHOLD` | 🆕 相似度阈值 (0.0-1.0) | 无 (不过滤) |
| `QDRANT_READ_ONLY` | 只读模式 | `false` |

### 嵌入模型配置 | Embedding Settings

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `EMBEDDING_PROVIDER` | `fastembed` 或 `openai_compatible` | `fastembed` |
| `EMBEDDING_MODEL` | 模型名称 | `sentence-transformers/all-MiniLM-L6-v2` |
| `OPENAI_API_KEY` | OpenAI 兼容 API 密钥 | 无 |
| `OPENAI_BASE_URL` | API 端点 | `https://api.openai.com/v1` |
| `OPENAI_VECTOR_SIZE` | 向量维度 | `1536` |

### 服务器配置 | Server Settings

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `PORT` / `FASTMCP_PORT` | 服务器端口 | `8765` |
| `LOG_LEVEL` | 日志级别 | `INFO` |

📖 **完整配置参考** | *Full reference:* [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md)

---

## 🎯 新功能：相似度阈值 | New: Score Threshold

**中文：** 通过设置最低相似度阈值，过滤掉不相关的搜索结果，提高结果质量。

**English:** Filter out irrelevant search results by setting a minimum similarity score threshold.

```env
# 推荐值 | Recommended values:
QDRANT_SCORE_THRESHOLD=0.3  # 宽松：更多结果 | Relaxed: more results
QDRANT_SCORE_THRESHOLD=0.5  # 平衡：推荐值 | Balanced: recommended
QDRANT_SCORE_THRESHOLD=0.7  # 严格：高相关度 | Strict: high relevance
```

📊 **详细说明** | *Detailed guide:* [`docs/SCORE_THRESHOLD_FEATURE.md`](docs/SCORE_THRESHOLD_FEATURE.md)

---

## 📦 集成示例 | Integration Examples

### Claude Desktop / Cursor / Windsurf

有两种配置方式 | *Two configuration methods:*

#### 方式 1：STDIO 模式（推荐）| Method 1: STDIO Mode (Recommended)

**优点** | *Advantages:*
- ✅ 无需预先启动服务器 | No need to start server manually
- ✅ 客户端自动管理服务器生命周期 | Client manages server lifecycle automatically
- ✅ 配置简单 | Simple configuration

**配置文件位置** | *Configuration file location:*
- **Cursor/Windsurf**: `%USERPROFILE%\.cursor\mcp.json` (Windows) 或 `~/.cursor/mcp.json` (macOS/Linux)
- **Claude Desktop**: `%APPDATA%\Claude\claude_desktop_config.json` (Windows) 或 `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

**配置示例** | *Configuration example:*

📖 **详细的 STDIO 配置教程**：[`docs/STDIO_CONFIGURATION_CN.md`](docs/STDIO_CONFIGURATION_CN.md)

查看配置示例 | *See configuration examples:*
- Windows Cursor: [`cursor_mcp_config_example_windows.json`](cursor_mcp_config_example_windows.json)
- macOS/Linux Cursor: [`cursor_mcp_config_example.json`](cursor_mcp_config_example.json)
- Claude Desktop: [`claude_desktop_config_example.json`](claude_desktop_config_example.json)

**Windows Cursor 配置示例：**
```json
{
  "mcpServers": {
    "qdrant-custom": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "C:\\AgentProjects\\mcp-qdrant-custom",
        "mcp-server-qdrant"
      ],
      "env": {
        "QDRANT_URL": "http://localhost:6333",
        "COLLECTION_NAME": "your-collection-name",
        "EMBEDDING_PROVIDER": "openai_compatible",
        "EMBEDDING_MODEL": "Qwen/Qwen3-Embedding-8B",
        "OPENAI_API_KEY": "sk-your-api-key-here",
        "OPENAI_BASE_URL": "https://api.siliconflow.cn/v1",
        "OPENAI_VECTOR_SIZE": "4096"
      }
    }
  }
}
```

**⚠️ 重要提示** | *Important Notes:*
- 将 `C:\\AgentProjects\\mcp-qdrant-custom` 替换为您的实际项目路径
- 如果 `uv` 不在 PATH 中，使用完整路径，如 `C:/Users/YOUR_USERNAME/AppData/Local/Microsoft/WinGet/Packages/astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe/uv.exe`
- Replace `C:\\AgentProjects\\mcp-qdrant-custom` with your actual project path
- If `uv` is not in PATH, use full path like `C:/Users/YOUR_USERNAME/AppData/Local/Microsoft/WinGet/Packages/astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe/uv.exe`

---

#### 方式 2：HTTP/SSE 模式 | Method 2: HTTP/SSE Mode

**适用场景** | *Use cases:*
- 远程访问 | Remote access
- 多客户端同时连接 | Multiple clients
- 调试和监控 | Debugging and monitoring

**步骤 1：启动服务器** | *Step 1: Start server*
```bash
# Windows
start_mcp_server.bat

# 或 Python 直接运行 | Or run with Python
uv run python run_http_server.py
```

**步骤 2：在 Cursor/Windsurf 中添加服务器** | *Step 2: Add server in Cursor/Windsurf:*
```
http://localhost:8765/sse
```

**说明** | *Note:*
- 默认端口为 `8765` (可通过 `.env` 中的 `PORT` 变量修改)
- 确保服务器已使用 `start_mcp_server.bat` 或 `run_http_server.py` 启动
- Default port is `8765` (can be changed via `PORT` in `.env`)
- Make sure server is running via `start_mcp_server.bat` or `run_http_server.py`

### VS Code

点击安装 | *Click to install:*

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=qdrant&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mcp-server-qdrant%22%5D%2C%22env%22%3A%7B%22QDRANT_URL%22%3A%22%24%7Binput%3AqdrantUrl%7D%22%2C%22QDRANT_API_KEY%22%3A%22%24%7Binput%3AqdrantApiKey%7D%22%2C%22COLLECTION_NAME%22%3A%22%24%7Binput%3AcollectionName%7D%22%7D%7D&inputs=%5B%7B%22type%22%3A%22promptString%22%2C%22id%22%3A%22qdrantUrl%22%2C%22description%22%3A%22Qdrant+URL%22%7D%2C%7B%22type%22%3A%22promptString%22%2C%22id%22%3A%22qdrantApiKey%22%2C%22description%22%3A%22Qdrant+API+Key%22%2C%22password%22%3Atrue%7D%2C%7B%22type%22%3A%22promptString%22%2C%22id%22%3A%22collectionName%22%2C%22description%22%3A%22Collection+Name%22%7D%5D)

---

## 🧪 测试 | Testing

```bash
# 快速测试 | Quick test
uv run python tests/quick_test.py

# 完整测试套件 | Full test suite
uv run pytest tests/

# 特定测试 | Specific tests
uv run python tests/test_score_threshold.py
uv run python tests/test_fastembed_integration.py
```

📋 **测试文档** | *Test documentation:* [`tests/README.md`](tests/README.md)

---

## 📚 文档索引 | Documentation

| 文档 | 说明 |
|------|------|
| [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md) | 完整配置指南 \| Complete configuration guide |
| [`docs/STDIO_CONFIGURATION_CN.md`](docs/STDIO_CONFIGURATION_CN.md) | 🆕 STDIO 模式配置（中文）\| STDIO mode configuration (Chinese) |
| [`docs/SCORE_THRESHOLD_FEATURE.md`](docs/SCORE_THRESHOLD_FEATURE.md) | 相似度阈值功能 \| Score threshold feature |
| [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) | 常见问题排查 \| Common troubleshooting |
| [`docs/DEBUGGING_GUIDE.md`](docs/DEBUGGING_GUIDE.md) | 深度调试指南 \| Deep debugging guide |
| [`docs/DOCKER_TROUBLESHOOTING.md`](docs/DOCKER_TROUBLESHOOTING.md) | Docker 问题排查 \| Docker troubleshooting |
| [`docs/QUICK_START_CN.md`](docs/QUICK_START_CN.md) | 中文快速开始 \| Chinese quick start |

---

## 🔧 传输协议 | Transport Protocols

```bash
# STDIO (默认，本地客户端) | STDIO (default, local clients)
uvx mcp-server-qdrant

# SSE (推荐，远程连接) | SSE (recommended, remote connections)
uvx mcp-server-qdrant --transport sse

# Streamable HTTP (现代协议) | Streamable HTTP (modern protocol)
uvx mcp-server-qdrant --transport streamable-http
```

---

## 🌐 嵌入模型提供商 | Embedding Providers

### 1. FastEmbed (本地，免费)
```env
EMBEDDING_PROVIDER=fastembed
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### 2. OpenAI
```env
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=text-embedding-3-small
OPENAI_API_KEY=sk-...
OPENAI_VECTOR_SIZE=1536
```

### 3. Ollama (本地)
```env
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=nomic-embed-text
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_VECTOR_SIZE=768
```

### 4. SiliconFlow (中国)
```env
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=Qwen/Qwen3-Embedding-8B
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
OPENAI_VECTOR_SIZE=4096
```

---

## 🐛 故障排查 | Troubleshooting

### 常见问题 | Common Issues

**服务器无法启动？** | *Server won't start?*
- 检查 `.env` 配置 | Check `.env` configuration
- 验证 Qdrant 连接 | Verify Qdrant connection
- 查看日志输出 | Check log output

**搜索结果不相关？** | *Irrelevant search results?*
- 调整 `QDRANT_SCORE_THRESHOLD` | Adjust score threshold
- 检查嵌入模型一致性 | Verify embedding model consistency
- 提高搜索限制 | Increase search limit

**嵌入错误？** | *Embedding errors?*
- 确认 API 密钥正确 | Confirm API key is correct
- 检查向量维度匹配 | Check vector size matches
- 验证 API 端点可访问 | Verify API endpoint is accessible

📖 **详细排查步骤** | *Detailed troubleshooting:* [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md)

---

## 🔐 安全注意事项 | Security Notes

⚠️ **重要** | *Important:*

1. **不要提交 `.env` 到版本控制** | *Never commit `.env` to version control*
2. **保护 API 密钥** | *Protect API keys*
3. **使用适当的文件权限** | *Use proper file permissions*
4. **生产环境使用密钥管理系统** | *Use secret management in production*

---

## 🤝 贡献 | Contributing

欢迎提交问题和功能请求！| *Issues and feature requests are welcome!*

### 本地开发 | Local Development

```bash
# 克隆仓库 | Clone repository
git clone <repository-url>
cd mcp-qdrant-custom

# 安装依赖 | Install dependencies
uv sync

# 运行开发服务器 | Run dev server
fastmcp dev src/mcp_server_qdrant/server.py

# 运行测试 | Run tests
uv run pytest
```

---

## 📄 许可证 | License

Apache License 2.0 - 详见 [`LICENSE`](LICENSE) 文件 | *See [`LICENSE`](LICENSE) file for details*

---

## 🔗 相关链接 | Related Links

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [FastEmbed](https://qdrant.github.io/fastembed/)

---

**制作者** | *Maintained by:* Your Name/Organization

**基于** | *Based on:* [mcp-server-qdrant](https://github.com/modelcontextprotocol/servers)
