# Troubleshooting Guide

This guide consolidates solutions to common issues encountered with the Qdrant MCP server.

---

## Issue: "No Results Found" from qdrant-find Tool

**Date Resolved**: 2024-10-21

### Symptoms
- `qdrant-find` tool returns "No results found"
- Qdrant database contains data (verified)
- Direct code search works but MCP tool fails

### Root Cause
**Server not configured with correct collection name** - The `COLLECTION_NAME` environment variable was not set when the server started, causing it to use a different/empty collection.

### Diagnosis Steps

1. **Verify data exists**:
```bash
curl http://localhost:6333/collections
```

2. **Check collection details**:
```bash
curl http://localhost:6333/collections/<collection-name>
```

3. **Test direct search**:
```python
import os
os.environ["COLLECTION_NAME"] = "your-collection-name"

from mcp_server_qdrant.mcp_server import QdrantMCPServer
from mcp_server_qdrant.settings import QdrantSettings, EmbeddingProviderSettings, ToolSettings

server = QdrantMCPServer(
    tool_settings=ToolSettings(),
    qdrant_settings=QdrantSettings(),
    embedding_provider_settings=EmbeddingProviderSettings(),
)

results = await server.qdrant_connector.search("test", limit=5)
```

4. **Check server configuration**:
```python
from mcp_server_qdrant.settings import QdrantSettings
settings = QdrantSettings()
print(f"Collection: {settings.collection_name}")
```

### Solution

**Restart the server with correct environment variables**:

```powershell
# PowerShell
$env:COLLECTION_NAME = "ws-fbaa5e241f1ea709"  # Your collection name
$env:QDRANT_URL = "http://localhost:6333"
$env:EMBEDDING_PROVIDER = "openai_compatible"
$env:EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-8B"
$env:OPENAI_VECTOR_SIZE = "4096"

uv run python run_http_server.py
```

Or use the startup script:
```powershell
powershell -File start_server_correct_config.ps1
```

### Verification

After restarting:
```bash
uv run python verify_fix.py
```

Expected output:
```
✓ Found 20 results for "embedding provider configuration"
✓ Found 20 results for "qdrant search query"
```

### Prevention

1. **Always set env vars** before starting server
2. **Use startup scripts** that set all required variables
3. **Verify configuration** after server starts
4. **Keep test script** to quickly verify server works

---

## Issue: Cursor MCP Tool Error

### Symptoms
- MCP tool works in tests but shows error in Cursor
- Error: `"MCP error -32602: Invalid request parameters"`

### Causes

1. **Cursor caching old connection**
2. **Server restarted but Cursor not reconnected**
3. **Schema mismatch** between Cursor and server

### Solution

**Restart Cursor** to refresh MCP server connection.

Alternative:
1. Open Cursor settings
2. Navigate to MCP Servers
3. Reload or reconnect the Qdrant server

---

## Issue: Vector Type Mismatch

### Symptoms
- Error: "Not existing vector name error"
- Store operation fails
- Collection exists but search fails

### Diagnosis

Check vector configuration:
```python
from qdrant_client import AsyncQdrantClient

client = AsyncQdrantClient(url="http://localhost:6333")
info = await client.get_collection("collection-name")
vectors_config = info.config.params.vectors

if isinstance(vectors_config, dict):
    print("Named vectors:", list(vectors_config.keys()))
else:
    print("Unnamed vectors")
```

### Root Cause

**Mismatch between collection vector type and server configuration**:
- **Collection uses**: Unnamed vectors
- **Server expects**: Named vectors (or vice versa)

### Solution

The code already handles both types automatically via `_uses_unnamed_vectors()` function. The issue is usually:

1. **Wrong collection**: Server pointing to different collection
2. **Configuration error**: Restart server with correct settings

**Fix**: Ensure `COLLECTION_NAME` matches the collection with data.

---

## Issue: Server Won't Start

### Symptoms
- Server fails to start
- Port already in use
- Import errors

### Diagnosis

**1. Check if port is in use**:
```powershell
netstat -ano | findstr :8765
```

**2. Kill existing process**:
```powershell
taskkill /F /PID <pid>
```

**3. Check Qdrant is running**:
```powershell
curl http://localhost:6333/healthz
```

**4. Verify dependencies**:
```bash
uv pip list
```

### Solution

**Complete restart procedure**:
```powershell
# 1. Stop old server
netstat -ano | findstr :8765
taskkill /F /PID <pid>

# 2. Verify Qdrant is running
curl http://localhost:6333/healthz

# 3. Start server with config
powershell -File start_server_correct_config.ps1
```

---

## Issue: Embedding Model Download Slow

### Symptoms
- First run takes very long
- "Downloading model..." message
- Connection timeouts

### Cause
Embedding models (FastEmbed or OpenAI-compatible) need to download on first use.

### Solution

**For FastEmbed**:
- Models download to cache (~100-500MB)
- Subsequent runs are fast
- Use smaller model: `sentence-transformers/all-MiniLM-L6-v2` (90MB)

**For OpenAI-compatible**:
- No downloads needed
- Models run on API server
- Check API connectivity

**Workaround**: Pre-download model:
```python
from fastembed import TextEmbedding
model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
# Model now cached
```

---

## Issue: Search Returns Irrelevant Results

### Symptoms
- Search completes but results don't match query
- Low relevance scores (<0.3)
- Wrong content returned

### Diagnosis

**1. Check if query matches data domain**:
```python
# If collection has code, search for code-related terms
# If collection has documents, search for document content
```

**2. Verify embedding model matches collection**:
```python
from mcp_server_qdrant.settings import EmbeddingProviderSettings
settings = EmbeddingProviderSettings()
print(f"Model: {settings.model_name}")
print(f"Vector size: {settings.openai_vector_size}")

# Compare with collection vector size
```

**3. Check collection data**:
```python
from qdrant_client import AsyncQdrantClient
client = AsyncQdrantClient(url="http://localhost:6333")
result = await client.scroll(
    collection_name="collection-name",
    limit=3,
    with_payload=True
)

for point in result[0]:
    print(point.payload)
```

### Solution

**Embedding model mismatch**:
- Collection created with model A
- Server using model B
- **Fix**: Use same model or recreate collection

**Data domain mismatch**:
- Collection has code, searching for general knowledge
- **Fix**: Populate with relevant data or adjust queries

---

## Issue: Windows Encoding Errors

### Symptoms
- `UnicodeEncodeError: 'gbk' codec can't encode character`
- Console output garbled
- Special characters fail

### Solution

**For Python scripts**:
```python
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
```

**For PowerShell**:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

**For batch files**:
```batch
chcp 65001
```

---

## Issue: SSE Connection Fails

### Symptoms
- `Connection refused` when using SSE client
- MCP server not responding
- Timeout errors

### Diagnosis

**1. Verify server is running**:
```powershell
netstat -ano | findstr :8765
```

**2. Check server logs**:
Look for startup messages indicating successful initialization.

**3. Test with curl**:
```bash
curl http://localhost:8765/sse
```

### Solution

**Server not running**:
```powershell
uv run python run_http_server.py
```

**Firewall blocking**:
- Allow Python through Windows Firewall
- Check if localhost is blocked

**Wrong port**:
- Verify `FASTMCP_PORT` environment variable
- Default is 8000, our config uses 8765

---

## Common Error Messages

### "ModuleNotFoundError: No module named 'mcp_server_qdrant'"

**Cause**: Running outside project context or dependencies not installed.

**Solution**:
```bash
cd project-root
uv sync
uv run python your_script.py
```

### "No such collection"

**Cause**: Collection name doesn't exist in Qdrant.

**Solution**:
1. Check collection exists: `curl http://localhost:6333/collections`
2. Create collection or use existing name
3. Update `COLLECTION_NAME` env var

### "Field 'collection_name' is required"

**Cause**: No default collection configured and none provided.

**Solution**:
```bash
export COLLECTION_NAME="your-collection"
# or
$env:COLLECTION_NAME = "your-collection"
```

---

## Quick Diagnostic Checklist

When something doesn't work:

- [ ] Is Qdrant running? (`curl http://localhost:6333/healthz`)
- [ ] Is MCP server running? (`netstat -ano | findstr :8765`)
- [ ] Are environment variables set? (`echo $env:COLLECTION_NAME`)
- [ ] Does the collection exist? (`curl http://localhost:6333/collections`)
- [ ] Does direct search work? (`uv run python verify_fix.py`)
- [ ] Are there any port conflicts? (`netstat -ano | findstr :8765`)
- [ ] Is the embedding model downloaded? (check for "Downloading..." messages)
- [ ] Are the vector dimensions correct? (collection vs model)

---

## Getting Help

If issues persist:

1. **Check logs**: Server startup logs show configuration
2. **Run diagnostics**: `uv run python quick_test.py`
3. **Review documentation**: `docs/DEBUGGING_GUIDE.md`
4. **Check test suite**: `uv run pytest tests/ -v`
5. **Verify configuration**: `docs/CONFIG.md`

---

## Related Documentation

- **Debugging Guide**: `DEBUGGING_GUIDE.md` - Detailed debugging process
- **Configuration**: `CONFIG.md` - Setup and configuration
- **Test Documentation**: `../tests/README.md` - Test suite info
- **Main README**: `../README.md` - Project overview

