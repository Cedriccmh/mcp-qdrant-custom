# Qdrant MCP Server 配置说明

## 配置方式

本项目支持两种配置方式：

### 方式 1: 直接修改 `start_mcp_server.bat`（推荐）

打开 `start_mcp_server.bat` 文件，在顶部的**配置区域**修改相应的环境变量：

```batch
REM ========================================
REM Configuration Section - 可在此修改配置
REM ========================================

REM Qdrant 配置
set QDRANT_URL=http://localhost:6333
REM 集合名称 - 可根据需要修改
set COLLECTION_NAME=your-collection-name

REM 嵌入模型配置
set EMBEDDING_PROVIDER=openai_compatible
set OPENAI_API_KEY=your-api-key-here
set OPENAI_BASE_URL=https://api.siliconflow.cn/v1
set EMBEDDING_MODEL=Qwen/Qwen3-Embedding-8B
set OPENAI_VECTOR_SIZE=4096
```

### 方式 2: 使用环境变量

也可以在系统环境变量或命令行中设置这些变量。

## 配置项说明

### Qdrant 服务器配置

| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `QDRANT_URL` | Qdrant 服务器地址 | - | `http://localhost:6333` |
| `COLLECTION_NAME` | 集合名称 | - | `my-collection` 或 `test-collection` |
| `QDRANT_API_KEY` | API 密钥（可选） | - | `your-api-key` |
| `QDRANT_SEARCH_LIMIT` | 搜索结果数量限制 | 10 | `20` |
| `QDRANT_READ_ONLY` | 只读模式 | false | `true` |

### 嵌入模型配置

| 变量名 | 说明 | 可选值 | 示例 |
|--------|------|--------|------|
| `EMBEDDING_PROVIDER` | 嵌入提供商类型 | `fastembed`, `openai_compatible` | `openai_compatible` |
| `EMBEDDING_MODEL` | 嵌入模型名称 | - | `Qwen/Qwen3-Embedding-8B` |

### OpenAI 兼容服务配置

当 `EMBEDDING_PROVIDER=openai_compatible` 时需要配置：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `OPENAI_API_KEY` | API 密钥 | `sk-xxx` |
| `OPENAI_BASE_URL` | API 基础 URL | `https://api.siliconflow.cn/v1` |
| `OPENAI_VECTOR_SIZE` | 向量维度 | `4096` |

**支持的服务提供商：**
- OpenAI API
- SiliconFlow
- Ollama (使用 `http://localhost:11434/v1`)
- 其他 OpenAI 兼容的服务

## 常见配置示例

### 示例 1: 使用不同的集合

```batch
set COLLECTION_NAME=my-custom-collection
```

### 示例 2: 使用 Ollama 本地服务

```batch
set EMBEDDING_PROVIDER=openai_compatible
set OPENAI_BASE_URL=http://localhost:11434/v1
set EMBEDDING_MODEL=nomic-embed-text
set OPENAI_VECTOR_SIZE=768
set OPENAI_API_KEY=ollama
```

### 示例 3: 使用 FastEmbed（无需 API 密钥）

```batch
set EMBEDDING_PROVIDER=fastembed
set EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### 示例 4: 连接到远程 Qdrant 服务器

```batch
set QDRANT_URL=https://your-cluster.qdrant.tech
set QDRANT_API_KEY=your-api-key
set COLLECTION_NAME=production-collection
```

## 注意事项

1. **集合名称** (`COLLECTION_NAME`) 必须与 Qdrant 服务器中已存在的集合匹配
2. **向量维度** (`OPENAI_VECTOR_SIZE`) 必须与选择的嵌入模型的输出维度一致
3. 修改配置后需要重启服务器才能生效
4. 确保 Qdrant 服务器正在运行并可访问

## 如何查看当前配置

运行 `start_mcp_server.bat` 时，会显示当前的配置信息：

```
Server Configuration:
  - Transport: HTTP/SSE
  - Port: 8765
  - URL: http://localhost:8765/sse
  - Storage: Qdrant HTTP Server (http://localhost:6333)
  - Collection: your-collection-name
  - Embedding Provider: openai_compatible
  - Embedding Model: Qwen/Qwen3-Embedding-8B
```


