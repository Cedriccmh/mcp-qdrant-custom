# Qdrant MCP Server - Debugging Guide

## Overview
This guide documents the debugging process and key learnings from resolving the "No results found" issue with the `qdrant-find` MCP tool.

---

## Problem Summary

**Symptom**: The `qdrant-find` MCP tool returned "No results found" even though the Qdrant database contained 776 code chunks.

**Root Cause**: The MCP server was not configured with the correct collection name (`COLLECTION_NAME` environment variable).

---

## Key Debugging Steps

### 1. **Verify Data Exists in Qdrant**

Always start by confirming the data actually exists:

```python
from qdrant_client import AsyncQdrantClient

client = AsyncQdrantClient(url="http://localhost:6333")
collections = await client.get_collections()

for coll in collections.collections:
    info = await client.get_collection(coll.name)
    print(f"{coll.name}: {info.points_count} points")
```

**Key Learning**: Don't assume the problem is in the code - verify the data exists first.

---

### 2. **Check Vector Configuration**

Vector type mismatch (named vs unnamed) can cause search failures:

```python
info = await client.get_collection("collection_name")
vectors_config = info.config.params.vectors

if isinstance(vectors_config, dict):
    print("Named vectors:", list(vectors_config.keys()))
else:
    print("Unnamed vectors")
```

**Key Learning**: The code in `qdrant.py` has logic to handle both types via `_uses_unnamed_vectors()`. If search fails, check if this detection is working.

---

### 3. **Test Direct Search (Bypass MCP)**

Create a test that initializes the server directly with explicit configuration:

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

results = await server.qdrant_connector.search("test query", limit=5)
```

**Key Learning**: If direct search works but MCP tool fails, the issue is configuration (environment variables) not code.

---

### 4. **Verify Running Server Configuration**

The running MCP server may have been started with different environment variables:

```python
# Check what the MCP tool schema shows
async with sse_client("http://localhost:8765/sse") as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()
        
        for tool in tools.tools:
            if tool.name == "qdrant-find":
                print("Parameters:", tool.inputSchema.get('properties', {}).keys())
                # If 'collection_name' is missing, server has default collection set
```

**Key Learning**: If `collection_name` is not in the schema, the server has a default collection configured via `make_partial_function`. But you can't determine WHICH collection from the MCP protocol alone.

---

### 5. **Check Environment Variable Propagation**

Environment variables set in batch files may not propagate correctly:

**Common Issues**:
- Server started before batch file set env vars
- Background processes don't inherit env vars
- Python script has fallback defaults that override

**Solution**: 
```powershell
# Set env vars in the SAME command that starts the server
$env:COLLECTION_NAME = "collection-name"
uv run python run_http_server.py
```

---

## Critical Configuration Points

### Environment Variables Priority

1. **Explicitly set in the same shell session** (highest priority)
2. **Set in batch/PowerShell script** that starts the server
3. **Fallback defaults in `run_http_server.py`** (lowest priority)

**Key Learning**: The `run_http_server.py` file has fallback defaults (line 12: `COLLECTION_NAME = "ws-77b2ac62ce00ae8e"`). These take effect if env vars aren't set BEFORE the server starts.

### Settings Class Behavior

The `QdrantSettings` class uses `pydantic_settings.BaseSettings`:

```python
collection_name: str | None = Field(
    default=None, validation_alias="COLLECTION_NAME"
)
```

- Reads from environment variable `COLLECTION_NAME`
- If not set, defaults to `None`
- If `None`, server may create a new collection or fail

---

## Testing Strategy

### Layer 1: Database Level
```python
# Test Qdrant directly
client = AsyncQdrantClient(url="http://localhost:6333")
results = await client.query_points(
    collection_name="collection-name",
    query=embedding_vector,
    limit=5
)
```

### Layer 2: Connector Level
```python
# Test QdrantConnector
connector = QdrantConnector(url, api_key, collection_name, embedding_provider)
results = await connector.search("query", limit=5)
```

### Layer 3: MCP Server Level
```python
# Test MCP Server directly
server = QdrantMCPServer(...)
results = await server.qdrant_connector.search("query", limit=5)
```

### Layer 4: MCP Protocol Level
```python
# Test via SSE client
async with sse_client("http://localhost:8765/sse") as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        result = await session.call_tool("qdrant-find", {"query": "test"})
```

**Key Learning**: Test from bottom to top. If lower layers work but higher layers fail, the issue is in configuration/communication, not core logic.

---

## Common Pitfalls

### 1. **Caching Issues**
- **Cursor**: May cache old MCP server connections → **Fix**: Restart Cursor
- **QdrantConnector**: Caches vector config detection → **Fix**: Restart server

### 2. **Vector Name Mismatch**
- Collection uses unnamed vectors but server configured for named vectors
- **Detection**: Check `_uses_unnamed_vectors()` return value
- **Fix**: Server code already handles this - just ensure using correct collection

### 3. **Multiple Collections with Similar Names**
- `ws-77b2ac62ce00ae8e` (old/default)
- `ws-fbaa5e241f1ea709` (actual data)
- **Fix**: Always verify which collection has the data

### 4. **Background Server Processes**
- Old server still running on port 8765
- **Detection**: `netstat -ano | findstr :8765`
- **Fix**: Kill old process before starting new one

---

## Debugging Checklist

When `qdrant-find` returns "No results found":

- [ ] Verify data exists in Qdrant (`client.get_collection()`)
- [ ] Check which collections exist (`client.get_collections()`)
- [ ] Verify vector configuration (named vs unnamed)
- [ ] Test direct search with QdrantConnector
- [ ] Check if server is using correct collection name
- [ ] Verify environment variables are set
- [ ] Confirm server process is the one you just started
- [ ] Test with MCP SSE client (bypass Cursor)
- [ ] Check server logs for initialization messages
- [ ] Verify embedding provider configuration matches collection

---

## Quick Diagnosis Script

```python
#!/usr/bin/env python3
"""Quick diagnostic script for Qdrant MCP issues"""
import asyncio
import os
from qdrant_client import AsyncQdrantClient

async def diagnose():
    print("=== QDRANT MCP DIAGNOSTICS ===\n")
    
    # 1. Check Qdrant
    print("1. Checking Qdrant collections...")
    client = AsyncQdrantClient(url="http://localhost:6333")
    collections = await client.get_collections()
    for coll in collections.collections:
        info = await client.get_collection(coll.name)
        print(f"   - {coll.name}: {info.points_count} points")
        print(f"     Vector type: {'Named' if isinstance(info.config.params.vectors, dict) else 'Unnamed'}")
    await client.close()
    
    # 2. Check env vars
    print("\n2. Checking environment variables...")
    print(f"   COLLECTION_NAME: {os.environ.get('COLLECTION_NAME', 'NOT SET')}")
    print(f"   QDRANT_URL: {os.environ.get('QDRANT_URL', 'NOT SET')}")
    print(f"   EMBEDDING_PROVIDER: {os.environ.get('EMBEDDING_PROVIDER', 'NOT SET')}")
    
    # 3. Check server config
    print("\n3. Checking server configuration...")
    from mcp_server_qdrant.settings import QdrantSettings, EmbeddingProviderSettings
    qdrant_settings = QdrantSettings()
    embedding_settings = EmbeddingProviderSettings()
    print(f"   QdrantSettings.collection_name: {qdrant_settings.collection_name}")
    print(f"   EmbeddingProvider: {embedding_settings.provider_type}")
    
    print("\n=== END DIAGNOSTICS ===")

if __name__ == "__main__":
    asyncio.run(diagnose())
```

---

## Resolution Pattern

**For "No results found" issues:**

1. **Verify** data exists → Test Layer 1 (Database)
2. **Isolate** the problem → Test Layers 2-4
3. **Identify** configuration issue → Check env vars and settings
4. **Fix** by restarting server with correct config
5. **Verify** fix works → Run full test suite

**Success Criteria**:
- ✓ Direct search returns results
- ✓ MCP tool via SSE returns results
- ✓ Results include file paths, scores, line numbers
- ✓ Cursor integration works (may need restart)

---

## Prevention

### Server Startup Best Practices

1. **Always use a startup script** (batch/PowerShell) that sets all env vars
2. **Verify env vars are set** before starting server
3. **Check for existing processes** on port 8765 before starting
4. **Log the configuration** on server startup
5. **Keep a test script** to verify server after startup

### Configuration Management

1. **Document the correct collection name** in CONFIG.md
2. **Use environment-specific configs** (dev, test, prod)
3. **Version control** startup scripts
4. **Monitor** collection names in Qdrant (they may change)

---

## Related Files

- `src/mcp_server_qdrant/qdrant.py` - Core search logic, unnamed vector detection
- `src/mcp_server_qdrant/settings.py` - Configuration classes
- `run_http_server.py` - Server startup with env var fallbacks
- `start_mcp_server.bat` - Batch file with configuration
- `start_server_correct_config.ps1` - PowerShell startup script

---

## Version History

- **2024-10-21**: Initial debugging guide created after resolving collection name configuration issue

