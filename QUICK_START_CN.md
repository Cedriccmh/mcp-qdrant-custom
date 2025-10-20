# MCP-Qdrant 快速开始指南

## 🎯 工具简介

MCP-Qdrant 是一个基于模型上下文协议（Model Context Protocol）的语义记忆服务器，它将 Qdrant 向量数据库与大语言模型（LLM）应用无缝集成，实现智能化的信息存储和检索。

### 核心功能
- **语义存储**：将信息转换为向量并存储到 Qdrant 数据库
- **智能检索**：基于语义相似度查找相关信息
- **元数据支持**：存储和检索附加的结构化数据

## 📦 安装前准备

### 1. 安装 Qdrant
```bash
# 使用 Docker 运行 Qdrant（推荐）
docker pull qdrant/qdrant
docker run -p 6333:6333 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

### 2. 确保已安装 Python 和 uv
```bash
# 安装 uv (Python 包管理器)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 🚀 快速安装

### 方式一：使用 uvx 直接运行（推荐）
```bash
# 设置环境变量并运行
QDRANT_URL="http://localhost:6333" \
COLLECTION_NAME="ws-77b2ac62ce00ae8e" \
uvx mcp-server-qdrant
```

### 方式二：Claude Desktop 集成
1. 找到配置文件位置：
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. 编辑配置文件，添加以下内容：
```json
{
  "mcpServers": {
    "qdrant": {
      "command": "uvx",
      "args": ["mcp-server-qdrant"],
      "env": {
        "QDRANT_URL": "http://localhost:6333",
        "COLLECTION_NAME": "ws-77b2ac62ce00ae8e",
        "EMBEDDING_MODEL": "sentence-transformers/all-MiniLM-L6-v2"
      }
    }
  }
}
```

3. 重启 Claude Desktop 应用

## ⚙️ 配置说明

### 必需配置
| 环境变量 | 说明 | 示例 |
|---------|------|------|
| `QDRANT_URL` 或 `QDRANT_LOCAL_PATH` | Qdrant 服务地址或本地路径 | `http://localhost:6333` |
| `COLLECTION_NAME` | 向量集合名称 | `ws-77b2ac62ce00ae8e` |

### 可选配置
| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `EMBEDDING_MODEL` | 嵌入模型名称 | `sentence-transformers/all-MiniLM-L6-v2` |
| `QDRANT_SEARCH_LIMIT` | 搜索返回数量 | `10` |
| `OPENAI_VECTOR_SIZE` | OpenAI 兼容服务的向量维度（仅在使用 `openai-compatible` 提供者时需要） | 根据模型自动确定 |

## 💡 使用示例

### 基础用法

#### 1. 存储信息
在 Claude Desktop 中使用：
```
请帮我记住：项目的API密钥存储在 /config/secrets.json 文件中，
需要使用 AES-256 加密算法进行解密。
```

MCP 工具会自动调用 `qdrant-store` 存储这条信息。

#### 2. 检索信息
```
我之前存储的 API 密钥相关信息是什么？
```

MCP 工具会调用 `qdrant-find` 进行语义搜索。

### 高级用法

#### 1. 带元数据的存储
```python
# 存储代码片段示例
information = "Python 函数用于连接数据库"
metadata = {
    "type": "code",
    "language": "python",
    "file": "db_utils.py",
    "code": """
    def connect_db(host, port, db_name):
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=db_name
        )
        return conn
    """
}
```

#### 2. 自定义嵌入模型

如果需要使用 OpenAI 兼容的嵌入模型：
```json
{
  "env": {
    "EMBEDDING_PROVIDER": "openai-compatible",
    "OPENAI_API_KEY": "your-api-key",
    "OPENAI_BASE_URL": "https://api.openai.com/v1",
    "EMBEDDING_MODEL": "text-embedding-3-small",
    "OPENAI_VECTOR_SIZE": "1536"
  }
}
```

## 🎨 常见使用场景

### 1. 个人知识管理
- 存储学习笔记、代码片段、技术文档
- 快速检索相关知识点

### 2. 项目文档管理
- 存储 API 文档、配置说明
- 跨项目知识共享

### 3. 代码库语义搜索
```bash
# 配置用于代码搜索
TOOL_STORE_DESCRIPTION="存储代码片段和功能描述" \
TOOL_FIND_DESCRIPTION="使用自然语言搜索代码功能" \
uvx mcp-server-qdrant
```

### 4. 对话上下文记忆
- 保存重要对话内容
- 构建长期记忆系统

## 🔍 验证安装

### 1. 检查服务状态
```bash
# 验证 Qdrant 是否运行
curl http://localhost:6333/health
```

### 2. 查看 Claude Desktop 工具
在 Claude Desktop 中输入：
```
列出所有可用的 MCP 工具
```

应该能看到 `qdrant-store` 和 `qdrant-find` 工具。

## 🐛 故障排除

### 问题1：连接失败
```bash
# 检查 Qdrant 服务
docker ps | grep qdrant

# 检查端口占用
netstat -an | grep 6333
```

### 问题2：嵌入模型下载慢
```bash
# 使用国内镜像或提前下载模型
export HF_ENDPOINT=https://hf-mirror.com
```

### 问题3：Claude Desktop 无法识别工具
1. 确认配置文件路径正确
2. 检查 JSON 语法是否正确
3. 重启 Claude Desktop 应用

## 📚 进阶配置

### 使用 Docker 部署
```bash
# 构建镜像
docker build -t mcp-qdrant .

# 运行容器
docker run -p 8000:8000 \
  -e FASTMCP_HOST="0.0.0.0" \
  -e QDRANT_URL="http://qdrant:6333" \
  -e COLLECTION_NAME="memories" \
  mcp-qdrant
```

### 远程访问配置
```bash
# 使用 SSE 传输协议
QDRANT_URL="http://localhost:6333" \
COLLECTION_NAME="my-collection" \
FASTMCP_PORT=8000 \
uvx mcp-server-qdrant --transport sse
```

## 🔗 相关链接

- [MCP 协议文档](https://modelcontextprotocol.io)
- [Qdrant 官方文档](https://qdrant.tech/documentation)
- [项目 GitHub](https://github.com/dazzaji/mcp-server-qdrant)

---

**提示**: 首次使用建议从本地 Qdrant 开始，熟悉后再迁移到云端服务。
