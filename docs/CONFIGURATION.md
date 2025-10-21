# Configuration Guide

Complete guide for configuring the MCP Server Qdrant.

---

## Quick Start

### Step 1: Copy the Template

**Windows (Command Prompt/PowerShell):**
```powershell
copy .env.example .env
```

**Windows (Git Bash) / Linux / macOS:**
```bash
cp .env.example .env
```

### Step 2: Edit with Your Values

Open `.env` and update these **minimum required settings**:

```env
# Qdrant Connection
QDRANT_URL=http://localhost:6333

# Collection
COLLECTION_NAME=your-collection-name

# Embeddings  
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=Qwen/Qwen3-Embedding-8B
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
OPENAI_VECTOR_SIZE=4096
```

### Step 3: Run Server

```bash
# Windows
start_mcp_server.bat

# Or use Python directly
uv run python run_http_server.py
```

**That's it!** ✅

---

## Environment Variables Reference

All configuration is managed through environment variables, which can be set in:
- A `.env` file in the project root (recommended)
- System environment variables
- Command line when starting the server

The `.env` file is automatically loaded by the application using `python-dotenv`.

### Qdrant Connection Settings

#### `QDRANT_URL`
- **Description**: URL of the Qdrant server
- **Type**: String (URL)
- **Default**: None
- **Required**: Yes (unless using `QDRANT_LOCAL_PATH`)
- **Example**: `http://localhost:6333`
- **Notes**: Cannot be used together with `QDRANT_LOCAL_PATH`

#### `QDRANT_API_KEY`
- **Description**: API key for Qdrant Cloud or secured instances
- **Type**: String
- **Default**: None
- **Required**: No
- **Example**: `your-api-key-here`
- **Notes**: Optional for local Qdrant instances

#### `QDRANT_LOCAL_PATH`
- **Description**: Path to local Qdrant storage directory
- **Type**: String (file path)
- **Default**: None
- **Required**: Yes (if not using `QDRANT_URL`)
- **Example**: `./qdrant_data`
- **Notes**: Cannot be used together with `QDRANT_URL` or `QDRANT_API_KEY`

#### `QDRANT_DATA_PATH`
- **Description**: Docker volume path for Qdrant data (for Docker deployments)
- **Type**: String (file path)
- **Default**: None
- **Required**: No
- **Example**: `./qdrant_data` or `/var/lib/qdrant`
- **Notes**: Only relevant for Docker deployments

### Collection Settings

#### `COLLECTION_NAME`
- **Description**: Default Qdrant collection name
- **Type**: String
- **Default**: None
- **Required**: No (tools will require collection name if not set)
- **Example**: `my-collection` or `test-collection`
- **Notes**: If set, the collection name is pre-filled in MCP tools

#### `QDRANT_SEARCH_LIMIT`
- **Description**: Maximum number of search results to return
- **Type**: Integer
- **Default**: `10`
- **Required**: No
- **Example**: `20`
- **Notes**: Higher values return more results but may impact performance

#### `QDRANT_READ_ONLY`
- **Description**: Enable read-only mode (prevents write operations)
- **Type**: Boolean (`true`/`false`, `1`/`0`)
- **Default**: `false`
- **Required**: No
- **Example**: `false`
- **Notes**: When enabled, only the `qdrant-find` tool is available

#### `QDRANT_SCORE_THRESHOLD`
- **Description**: Minimum similarity score threshold for search results
- **Type**: Float (0.0-1.0 for cosine similarity)
- **Default**: None (no filtering)
- **Required**: No
- **Example**: `0.5`
- **Notes**: 
  - Results with scores below this threshold will be filtered out
  - For cosine similarity (used by default), scores range from -1 to 1, with 1 being most similar
  - Recommended range: 0.3-0.7
  - Lower values (e.g., 0.3) return more results but may include less relevant matches
  - Higher values (e.g., 0.7) return fewer, more relevant results
  - If not set, all results up to `QDRANT_SEARCH_LIMIT` are returned

#### `QDRANT_ALLOW_ARBITRARY_FILTER`
- **Description**: Allow arbitrary filter queries
- **Type**: Boolean (`true`/`false`, `1`/`0`)
- **Default**: `false`
- **Required**: No
- **Example**: `false`
- **Notes**: Advanced feature for custom filtering

### Embedding Provider Settings

#### `EMBEDDING_PROVIDER`
- **Description**: Type of embedding provider to use
- **Type**: String (enum)
- **Default**: `fastembed`
- **Required**: No
- **Allowed Values**:
  - `fastembed` - Local FastEmbed models (no API key required)
  - `openai_compatible` - OpenAI or compatible APIs (Ollama, Azure, etc.)
- **Example**: `openai_compatible`

#### `EMBEDDING_MODEL`
- **Description**: Name of the embedding model
- **Type**: String
- **Default**: `sentence-transformers/all-MiniLM-L6-v2` (for FastEmbed)
- **Required**: No
- **Examples**:
  - FastEmbed: `sentence-transformers/all-MiniLM-L6-v2`
  - OpenAI: `text-embedding-ada-002`, `text-embedding-3-small`, `text-embedding-3-large`
  - Ollama: `nomic-embed-text`, `mxbai-embed-large`
  - SiliconFlow: `Qwen/Qwen3-Embedding-8B`

### OpenAI Compatible Settings

These settings apply when `EMBEDDING_PROVIDER=openai_compatible`.

#### `OPENAI_API_KEY`
- **Description**: API key for OpenAI or compatible services
- **Type**: String
- **Default**: None
- **Required**: Yes (for OpenAI compatible provider)
- **Examples**:
  - OpenAI: `sk-...`
  - SiliconFlow: `sk-...`
  - Ollama: Can be omitted or any value
- **Notes**: Some providers like local Ollama don't require a real key

#### `OPENAI_BASE_URL`
- **Description**: Base URL for the embedding API
- **Type**: String (URL)
- **Default**: `https://api.openai.com/v1`
- **Required**: No
- **Examples**:
  - OpenAI: `https://api.openai.com/v1` (default)
  - Ollama: `http://localhost:11434/v1`
  - Azure OpenAI: `https://your-resource.openai.azure.com/openai/deployments/your-deployment`
  - SiliconFlow: `https://api.siliconflow.cn/v1`
- **Notes**: Must include `/v1` suffix for OpenAI-compatible APIs

#### `OPENAI_VECTOR_SIZE`
- **Description**: Vector dimension size for the embedding model
- **Type**: Integer
- **Default**: `1536`
- **Required**: Yes (for OpenAI compatible provider)
- **Common Values**:
  - OpenAI text-embedding-ada-002: `1536`
  - OpenAI text-embedding-3-small: `1536`
  - OpenAI text-embedding-3-large: `3072`
  - Qwen/Qwen3-Embedding-8B: `4096`
  - nomic-embed-text (Ollama): `768`
- **Notes**: Must match the actual vector size of your model

#### `OPENAI_TIMEOUT`
- **Description**: Request timeout in seconds for API calls
- **Type**: Float
- **Default**: `30.0`
- **Required**: No
- **Example**: `30.0`
- **Notes**: Increase for slow connections or large batches

### Server Settings

#### `PORT`
- **Description**: Port for HTTP/SSE server
- **Type**: Integer
- **Default**: `8765`
- **Required**: No
- **Example**: `8765`
- **Notes**: Only used for HTTP/SSE transport, not stdio

#### `FASTMCP_PORT`
- **Description**: FastMCP server port
- **Type**: Integer
- **Default**: `8765`
- **Required**: No
- **Example**: `8765`
- **Notes**: Usually set to same value as `PORT`

#### `PYTHONUNBUFFERED`
- **Description**: Python unbuffered output mode
- **Type**: Integer (`1` or `0`)
- **Default**: None
- **Required**: No (but recommended)
- **Example**: `1`
- **Notes**: Recommended to set to `1` for real-time logging

### Logging Settings

#### `LOG_LEVEL`
- **Description**: Logging level for the application
- **Type**: String (enum)
- **Default**: `INFO`
- **Required**: No
- **Allowed Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Example**: `DEBUG`
- **Notes**: Use `DEBUG` for troubleshooting, `INFO` for production

### Tool Descriptions (Advanced)

#### `TOOL_STORE_DESCRIPTION`
- **Description**: Custom description for the `qdrant-store` tool
- **Type**: String
- **Default**: "Keep the memory for later use, when you are asked to remember something."
- **Required**: No
- **Notes**: Customize how AI assistants understand the store tool

#### `TOOL_FIND_DESCRIPTION`
- **Description**: Custom description for the `qdrant-find` tool
- **Type**: String
- **Default**: "Look up memories in Qdrant..."
- **Required**: No
- **Notes**: Customize how AI assistants understand the find tool

---

## Configuration Examples

### Example 1: Local Qdrant with OpenAI Embeddings

```env
# Qdrant Connection
QDRANT_URL=http://localhost:6333

# Collection
COLLECTION_NAME=my_memories

# Embeddings
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=text-embedding-3-small
OPENAI_API_KEY=sk-your-openai-key
OPENAI_VECTOR_SIZE=1536

# Server
PORT=8765
LOG_LEVEL=INFO
```

### Example 2: Qdrant Cloud with FastEmbed (No API Key)

```env
# Qdrant Connection
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-cloud-key

# Collection
COLLECTION_NAME=embeddings

# Embeddings (local, no API key needed)
EMBEDDING_PROVIDER=fastembed
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Server
PORT=8765
LOG_LEVEL=INFO
```

### Example 3: Local Ollama with Local Qdrant Storage

```env
# Qdrant Connection (local file storage)
QDRANT_LOCAL_PATH=./qdrant_data

# Collection
COLLECTION_NAME=ollama_embeddings

# Embeddings (Ollama local)
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=nomic-embed-text
OPENAI_API_KEY=not-needed
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_VECTOR_SIZE=768

# Server
PORT=8765
LOG_LEVEL=DEBUG
```

### Example 4: SiliconFlow with Docker Qdrant

```env
# Qdrant Connection
QDRANT_URL=http://localhost:6333
QDRANT_DATA_PATH=./qdrant_data

# Collection
COLLECTION_NAME=siliconflow_embeddings
QDRANT_SEARCH_LIMIT=20

# Embeddings (SiliconFlow API)
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_MODEL=Qwen/Qwen3-Embedding-8B
OPENAI_API_KEY=sk-your-siliconflow-key
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
OPENAI_VECTOR_SIZE=4096

# Server
PORT=8765
PYTHONUNBUFFERED=1
LOG_LEVEL=DEBUG
```

---

## Quick Reference Tables

### Most Common Settings

| Setting | Purpose | Example |
|---------|---------|---------|
| `QDRANT_URL` | Qdrant server location | `http://localhost:6333` |
| `COLLECTION_NAME` | Collection to use | `my-collection` |
| `EMBEDDING_PROVIDER` | Embedding type | `openai_compatible` |
| `EMBEDDING_MODEL` | Model name | `Qwen/Qwen3-Embedding-8B` |
| `OPENAI_API_KEY` | API key | `sk-...` |
| `OPENAI_BASE_URL` | API endpoint | `https://api.siliconflow.cn/v1` |
| `OPENAI_VECTOR_SIZE` | Vector dimensions | `4096` |
| `PORT` | Server port | `8765` |

### Embedding Provider Options

| Provider | API Key Required | Local | Example Model |
|----------|-----------------|-------|---------------|
| `fastembed` | No | Yes | `sentence-transformers/all-MiniLM-L6-v2` |
| `openai_compatible` (OpenAI) | Yes | No | `text-embedding-3-small` |
| `openai_compatible` (Ollama) | No | Yes | `nomic-embed-text` |
| `openai_compatible` (SiliconFlow) | Yes | No | `Qwen/Qwen3-Embedding-8B` |

### Common Vector Sizes

| Model | Vector Size |
|-------|------------|
| `sentence-transformers/all-MiniLM-L6-v2` | 384 |
| `nomic-embed-text` | 768 |
| `text-embedding-ada-002` | 1536 |
| `text-embedding-3-small` | 1536 |
| `text-embedding-3-large` | 3072 |
| `Qwen/Qwen3-Embedding-8B` | 4096 |

---

## Troubleshooting

### Configuration not loading?

1. Ensure `.env` file is in the project root directory
2. Check that the file is named exactly `.env` (not `.env.txt` or similar)
3. Verify there are no syntax errors in `.env` (no quotes around values needed)
4. Check file permissions - ensure the file is readable

### Which configuration is being used?

The settings loading priority is:
1. System environment variables (highest priority)
2. `.env` file in project root
3. Default values in code (lowest priority)

### Validating your configuration

Run the quick test script to validate your setup:
```bash
uv run python quick_test.py
```

Or check the logs when starting the server - you should see:
```
[Settings] Loaded environment from C:\path\to\.env
```

---

## Security Notes

⚠️ **Important Security Considerations**:

1. **Never commit `.env` to version control**
   - The `.env` file is already in `.gitignore`
   - Only commit `.env.example` with placeholder values

2. **Protect API keys**
   - Treat `OPENAI_API_KEY` and `QDRANT_API_KEY` as secrets
   - Rotate keys if they are accidentally exposed

3. **File permissions**
   - On Unix systems, set `.env` to 600 (read/write for owner only)
   - On Windows, use file system ACLs to restrict access

4. **Production deployments**
   - Consider using secret management systems (e.g., AWS Secrets Manager, Azure Key Vault)
   - Use environment variables from your deployment platform instead of `.env` files

---

## Support

For more information:
- [README.md](../README.md) - General documentation
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [DEBUGGING_GUIDE.md](DEBUGGING_GUIDE.md) - Deep debugging methodology

For issues and questions, please visit the project repository.