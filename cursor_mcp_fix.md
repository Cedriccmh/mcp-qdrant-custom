# Cursor MCP Qdrant Issue Analysis & Solution

## 🔍 Root Cause Identified

The MCP server is **properly configured and tools are registered**, but there's a **Windows-specific stdin pipe communication issue** preventing Cursor from communicating with the server via stdio transport.

### Test Results:
- ✅ Server imports and initializes correctly
- ✅ Tools are properly registered (qdrant-find, qdrant-store)
- ✅ FastMCP structure is correct
- ❌ **Stdin pipe fails with `OSError: [Errno 22] Invalid argument`** on Windows

## 🛠️ Solution: Use Alternative Transport

Since stdio transport has issues on Windows, we have two options:

### Option 1: Use HTTP Transport (Recommended)

Create a new file `run_http_server.py`:

```python
#!/usr/bin/env python3
import os
import sys

# Set environment variables
os.environ["QDRANT_URL"] = ":memory:"
os.environ["COLLECTION_NAME"] = "ws-77b2ac62ce00ae8e"
os.environ["EMBEDDING_PROVIDER"] = "openai_compatible"
os.environ["OPENAI_API_KEY"] = "sk-jdunbqgibzuvmglufzuluzkqxbmxtoxburabdusipasieufv"
os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"
os.environ["EMBEDDING_MODEL"] = "Qwen/Qwen3-Embedding-8B"
os.environ["OPENAI_VECTOR_SIZE"] = "4096"

from mcp_server_qdrant.server import mcp

# Run with SSE transport on a local port
mcp.run(transport="sse", port=8765)
```

Then update your Cursor config to connect via HTTP:

```json
{
  "mcpServers": {
    "qdrant": {
      "url": "http://localhost:8765/sse"
    }
  }
}
```

### Option 2: Use npx/uvx Package Manager

Try installing and running via uvx (if the package is published):

```json
{
  "mcpServers": {
    "qdrant": {
      "command": "uvx",
      "args": ["mcp-server-qdrant"]
    }
  }
}
```

### Option 3: Create a Wrapper Script

Create `mcp_wrapper.py` that handles the communication better:

```python
#!/usr/bin/env python3
import sys
import os

# Force unbuffered I/O
sys.stdin = os.fdopen(sys.stdin.fileno(), 'rb', 0)
sys.stdout = os.fdopen(sys.stdout.fileno(), 'wb', 0)

# Set environment
os.environ.update({
    "QDRANT_URL": ":memory:",
    "COLLECTION_NAME": "ws-77b2ac62ce00ae8e",
    "EMBEDDING_PROVIDER": "openai_compatible",
    "OPENAI_API_KEY": "sk-jdunbqgibzuvmglufzuluzkqxbmxtoxburabdusipasieufv",
    "OPENAI_BASE_URL": "https://api.siliconflow.cn/v1",
    "EMBEDDING_MODEL": "Qwen/Qwen3-Embedding-8B",
    "OPENAI_VECTOR_SIZE": "4096",
    "PYTHONUNBUFFERED": "1"
})

# Import and run
from mcp_server_qdrant.main import main
main()
```

## 📝 Current Working Configuration

Based on testing, here's what works:

1. **Server Structure**: ✅ Correctly implemented
2. **Tools Registration**: ✅ 2 tools properly registered
3. **FastMCP Integration**: ✅ Working correctly
4. **Windows stdio**: ❌ Has pipe communication issues

## 🚀 Recommended Next Steps

1. **Try the HTTP/SSE transport** instead of stdio
2. **Run the server as a background service** using the HTTP transport
3. **Check if there's a PyPI/npm package** that can be installed via uvx/npx

## 🐛 Technical Details

The issue occurs because:
- Windows handles subprocess pipes differently than Unix systems
- The MCP server's stdio implementation may not be fully compatible with Windows pipe handling
- The error `[Errno 22] Invalid argument` occurs when trying to write to or flush the stdin pipe

This is likely a FastMCP or MCP protocol library issue on Windows that needs to be addressed upstream.
