# STDIO 模式配置指南（本地自定义项目）

本文档说明如何在 **Cursor/Windsurf/Claude Desktop** 中配置 `mcp-qdrant-custom` 项目的 STDIO 模式，实现无需手动启动服务器即可使用。

---

## 📌 什么是 STDIO 模式？

STDIO（标准输入输出）模式是 MCP 服务器的一种传输方式：
- ✅ **自动启动**：客户端在需要时自动启动服务器进程
- ✅ **生命周期管理**：客户端关闭时自动停止服务器
- ✅ **无需预启动**：不需要运行 `start_mcp_server.bat`
- ✅ **配置简单**：只需配置一次，之后自动工作

---

## 🎯 适用场景

### ✅ 适合使用 STDIO 模式：
- 本地开发和使用
- 单个客户端（Claude Desktop/Cursor）
- 希望简化启动流程
- 个人使用场景

### ❌ 不适合 STDIO 模式：
- 需要远程访问
- 多个客户端同时连接
- 需要独立监控服务器状态
- 生产环境部署

对于以上场景，请使用 [HTTP/SSE 模式](../README.md#方式-2httpsee-模式--method-2-httpsse-mode)。

---

## 🚀 配置步骤

### 步骤 1：确认项目已安装

```bash
cd C:\AgentProjects\mcp-qdrant-custom
uv sync
```

这会安装项目依赖并以可编辑模式安装项目本身。

### 步骤 2：找到配置文件

#### Cursor/Windsurf
- **Windows**: `%USERPROFILE%\.cursor\mcp.json`
- **macOS/Linux**: `~/.cursor/mcp.json`

#### Claude Desktop
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### 步骤 3：编辑配置文件

#### 🪟 Windows 配置

**选项 A：`uv` 在 PATH 中（推荐）**

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

**选项 B：使用 `uv` 的完整路径**

如果 `uv` 不在 PATH 中，找到 `uv.exe` 的完整路径：

```powershell
# 在 PowerShell 中运行
where.exe uv
```

通常路径为：
```
C:\Users\YOUR_USERNAME\AppData\Local\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe
```

配置示例：

```json
{
  "mcpServers": {
    "qdrant-custom": {
      "command": "C:/Users/YOUR_USERNAME/AppData/Local/Microsoft/WinGet/Packages/astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe/uv.exe",
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

**⚠️ 注意：**
- `command` 中使用正斜杠 `/` 或反斜杠 `\\` 都可以
- `--directory` 参数中必须使用双反斜杠 `\\`

#### 🍎 macOS/Linux 配置

```json
{
  "mcpServers": {
    "qdrant-custom": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/mcp-qdrant-custom",
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

### 步骤 4：配置环境变量

根据您的需求修改 `env` 部分：

| 环境变量 | 必需 | 说明 | 示例 |
|---------|------|------|------|
| `QDRANT_URL` | ✅ | Qdrant 服务器地址 | `http://localhost:6333` |
| `COLLECTION_NAME` | ✅ | 集合名称 | `my-collection` |
| `EMBEDDING_PROVIDER` | ❌ | 嵌入提供商 | `openai_compatible` 或 `fastembed` |
| `EMBEDDING_MODEL` | ❌ | 模型名称 | `Qwen/Qwen3-Embedding-8B` |
| `OPENAI_API_KEY` | ⚠️ | API 密钥（使用 OpenAI 兼容时必需） | `sk-...` |
| `OPENAI_BASE_URL` | ❌ | API 端点 | `https://api.siliconflow.cn/v1` |
| `OPENAI_VECTOR_SIZE` | ⚠️ | 向量维度（使用 OpenAI 兼容时必需） | `4096` |

完整的环境变量说明请参考 [CONFIGURATION.md](CONFIGURATION.md)。

### 步骤 5：重启客户端

- **Cursor/Windsurf**: 完全关闭并重新打开
- **Claude Desktop**: 退出并重新启动应用

---

## ✅ 验证配置

### 方法 1：在客户端中测试

在 Cursor 或 Claude Desktop 中，尝试使用 MCP 工具：

```
请存储这条信息：今天是测试日
```

如果配置正确，工具应该能正常工作。

### 方法 2：查看日志（Cursor）

在 Cursor 中：
1. 打开命令面板（Ctrl+Shift+P）
2. 搜索 "MCP"
3. 查看 MCP 服务器状态和日志

### 方法 3：手动测试命令

在终端中测试配置的命令是否能运行：

```powershell
# Windows - 测试 uv run 命令
cd C:\AgentProjects\mcp-qdrant-custom
uv run mcp-server-qdrant --help
```

应该能看到帮助信息而不是错误。

---

## 🐛 常见问题

### 问题 1：找不到 `uv` 命令

**症状**：客户端报错 "command not found: uv"

**解决方案**：
1. 检查 `uv` 是否安装：
   ```powershell
   where.exe uv
   ```
2. 如果未安装，安装 uv：
   ```powershell
   winget install astral-sh.uv
   ```
3. 或者使用 `uv` 的完整路径（见上文"选项 B"）

### 问题 2：找不到模块 `mcp_server_qdrant`

**症状**：错误信息包含 "No module named 'mcp_server_qdrant'"

**原因**：项目未以可编辑模式安装

**解决方案**：
```bash
cd C:\AgentProjects\mcp-qdrant-custom
uv sync
```

验证安装：
```bash
uv pip list | findstr mcp-server-qdrant
```

应该显示：
```
mcp-server-qdrant  0.8.0  C:\AgentProjects\mcp-qdrant-custom
```

### 问题 3：连接 Qdrant 失败

**症状**：错误信息包含 "Connection refused" 或 "Cannot connect to Qdrant"

**解决方案**：
1. 确认 Qdrant 正在运行：
   ```bash
   curl http://localhost:6333/health
   ```
2. 如果未运行，启动 Qdrant：
   ```bash
   docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
   ```

### 问题 4：环境变量未生效

**症状**：服务器使用了错误的集合或配置

**原因**：可能存在 `.env` 文件覆盖了配置

**解决方案**：
1. 检查项目根目录是否有 `.env` 文件
2. 删除或重命名该文件（STDIO 模式不使用 `.env`）
3. 所有配置都应在 `mcp.json` 的 `env` 部分

**配置优先级**：
```
mcp.json 中的 env > 系统环境变量 > .env 文件
```

### 问题 5：路径包含空格

**症状**：路径解析错误

**解决方案**：
- Windows：使用双引号包裹路径，并使用双反斜杠
  ```json
  "C:\\Users\\My Name\\Projects\\mcp-qdrant-custom"
  ```
- 或者使用短路径（8.3 格式）
- 建议：避免在项目路径中使用空格

---

## 🔄 切换到 HTTP/SSE 模式

如果 STDIO 模式不适合您的使用场景，可以切换到 HTTP/SSE 模式：

1. 从 `mcp.json` 中删除或注释 `qdrant-custom` 配置
2. 运行服务器：
   ```bash
   start_mcp_server.bat
   ```
3. 在 Cursor 中添加 SSE 服务器：`http://localhost:8765/sse`

详细说明请参考 [README.md](../README.md#方式-2httpsee-模式--method-2-httpsse-mode)。

---

## 📋 配置模板

完整的配置模板文件：
- Windows: [`cursor_mcp_config_example_windows.json`](../cursor_mcp_config_example_windows.json)
- macOS/Linux: [`cursor_mcp_config_example.json`](../cursor_mcp_config_example.json)
- Claude Desktop: [`claude_desktop_config_example.json`](../claude_desktop_config_example.json)

---

## 🆚 STDIO vs HTTP/SSE 对比

| 特性 | STDIO 模式 | HTTP/SSE 模式 |
|------|-----------|---------------|
| **启动方式** | 自动启动 | 手动启动 |
| **配置复杂度** | 简单 | 中等 |
| **远程访问** | ❌ 不支持 | ✅ 支持 |
| **多客户端** | ❌ 单客户端 | ✅ 多客户端 |
| **调试难度** | 较难 | 容易 |
| **推荐场景** | 个人本地使用 | 团队/远程使用 |

---

## 📚 相关文档

- [完整配置指南](CONFIGURATION.md) - 所有环境变量说明
- [故障排查指南](TROUBLESHOOTING.md) - 常见问题解决
- [主 README](../README.md) - 项目概述

---

**最后更新**：2025-10-26

