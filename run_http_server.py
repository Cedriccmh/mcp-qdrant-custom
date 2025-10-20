#!/usr/bin/env python3
"""Run MCP server with HTTP/SSE transport to avoid Windows stdio issues"""
import os
import sys

# Set environment variables
# Only set defaults if not already set by the batch file
if "QDRANT_URL" not in os.environ and "QDRANT_LOCAL_PATH" not in os.environ:
    os.environ["QDRANT_URL"] = "http://localhost:6333"

if "COLLECTION_NAME" not in os.environ:
    os.environ["COLLECTION_NAME"] = "ws-77b2ac62ce00ae8e"

if "EMBEDDING_PROVIDER" not in os.environ:
    os.environ["EMBEDDING_PROVIDER"] = "openai_compatible"

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "sk-jdunbqgibzuvmglufzuluzkqxbmxtoxburabdusipasieufv"

if "OPENAI_BASE_URL" not in os.environ:
    os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"

if "EMBEDDING_MODEL" not in os.environ:
    os.environ["EMBEDDING_MODEL"] = "Qwen/Qwen3-Embedding-8B"

if "OPENAI_VECTOR_SIZE" not in os.environ:
    os.environ["OPENAI_VECTOR_SIZE"] = "4096"

if "QDRANT_SEARCH_LIMIT" not in os.environ:
    os.environ["QDRANT_SEARCH_LIMIT"] = "20"

print("Starting MCP server with SSE transport on port 8765...")
print("Configure Cursor to connect to: http://localhost:8765/sse")
print("")

from mcp_server_qdrant.server import mcp

# Run with SSE transport
try:
    mcp.run(transport="sse", port=8765)
except KeyboardInterrupt:
    print("\nServer stopped.")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
