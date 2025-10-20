# 配置 OpenAI Compatible Embedding Models

本项目现在支持 OpenAI 兼容的 embedding 模型！你可以使用 OpenAI、Azure OpenAI、Ollama 或任何其他兼容 OpenAI API 的服务。

## 核心设计

项目通过 `QdrantMCPServer` 的 `embedding_provider` 参数支持自定义 embedding provider，这是一个非常灵活的扩展点。

## 使用方法

### 方法 1：使用内置支持（推荐）

通过环境变量配置：

```bash
# OpenAI
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_VECTOR_SIZE=1536

# Ollama (本地运行)
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=nomic-embed-text
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_VECTOR_SIZE=768

# Azure OpenAI
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_API_KEY=your-azure-key
OPENAI_BASE_URL=https://your-resource.openai.azure.com/openai/deployments/your-deployment
OPENAI_VECTOR_SIZE=1536

# 其他 Qdrant 配置
QDRANT_URL=http://localhost:6333
COLLECTION_NAME=my-collection
```

运行服务器：
```bash
uvx mcp-server-qdrant
```

### 方法 2：使用自定义服务器（更灵活）

运行自定义服务器：

```bash
# 设置 OpenAI 配置
export OPENAI_API_KEY="your-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_MODEL_NAME="text-embedding-ada-002"
export OPENAI_VECTOR_SIZE="1536"

# 设置 Qdrant 配置
export QDRANT_URL="http://localhost:6333"
export COLLECTION_NAME="my-collection"

# 运行自定义服务器
python -m mcp_server_qdrant.custom_server --transport sse
```

### 方法 3：编程方式（最大灵活性）

```python
from mcp_server_qdrant.mcp_server import QdrantMCPServer
from mcp_server_qdrant.settings import QdrantSettings, ToolSettings
from mcp_server_qdrant.embeddings.openai_compatible import OpenAICompatibleProvider

# 创建自定义 embedding provider
embedding_provider = OpenAICompatibleProvider(
    model_name="text-embedding-ada-002",
    api_key="your-api-key",
    base_url="https://api.openai.com/v1",
    vector_size=1536
)

# 创建服务器，直接注入 provider
mcp = QdrantMCPServer(
    tool_settings=ToolSettings(),
    qdrant_settings=QdrantSettings(),
    embedding_provider=embedding_provider,  # 关键：直接注入自定义 provider
)

# 运行服务器
mcp.run()
```

## 支持的服务

### OpenAI
```bash
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=text-embedding-ada-002  # 或 text-embedding-3-small, text-embedding-3-large
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_VECTOR_SIZE=1536  # ada-002: 1536, 3-small: 1536, 3-large: 3072
```

### Ollama（本地模型）
```bash
# 首先运行 Ollama
ollama pull nomic-embed-text  # 或其他 embedding 模型
ollama serve

# 配置
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=nomic-embed-text
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_VECTOR_SIZE=768  # 根据模型而定
```

### Azure OpenAI
```bash
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_API_KEY=your-azure-api-key
OPENAI_BASE_URL=https://your-resource.openai.azure.com/openai/deployments/your-deployment-name
OPENAI_VECTOR_SIZE=1536
```

### 其他兼容服务

任何支持 OpenAI API 格式的服务都可以使用，例如：
- FastChat
- Text Generation Inference (TGI)
- LocalAI
- 等等

## 常见模型的向量维度

| 模型 | 向量维度 |
|-----|---------|
| text-embedding-ada-002 | 1536 |
| text-embedding-3-small | 1536 |
| text-embedding-3-large | 3072 |
| nomic-embed-text | 768 |
| all-MiniLM-L6-v2 | 384 |
| bge-large-zh | 1024 |

## 在 Claude Desktop 中使用

更新 `claude_desktop_config.json`：

```json
{
  "qdrant": {
    "command": "uvx",
    "args": ["mcp-server-qdrant"],
    "env": {
      "QDRANT_URL": "http://localhost:6333",
      "COLLECTION_NAME": "ws-77b2ac62ce00ae8e",
      "EMBEDDING_PROVIDER": "openai_compatible",
      "EMBEDDING_MODEL": "text-embedding-ada-002",
      "OPENAI_API_KEY": "your-api-key",
      "OPENAI_BASE_URL": "https://api.openai.com/v1",
      "OPENAI_VECTOR_SIZE": "1536"
    }
  }
}
```

## 故障排查

1. **连接错误**：确保 API 端点可访问
2. **认证错误**：检查 API key 是否正确
3. **向量维度不匹配**：确保 `OPENAI_VECTOR_SIZE` 与实际模型输出匹配
4. **超时错误**：增加 timeout 设置或使用更快的端点

## 架构优势

- **无需修改源码**：通过依赖注入直接使用自定义 provider
- **灵活扩展**：可以轻松添加任何 embedding 服务
- **向后兼容**：不影响现有的 FastEmbed 支持
- **类型安全**：所有 provider 都实现相同的抽象接口
