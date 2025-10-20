#!/usr/bin/env python3
"""测试 MCP 协议通信"""
import json
import os
import sys

# 设置环境变量
os.environ["QDRANT_URL"] = ":memory:"
os.environ["COLLECTION_NAME"] = "test"
os.environ["EMBEDDING_PROVIDER"] = "openai_compatible"
os.environ["OPENAI_API_KEY"] = "sk-test"
os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"
os.environ["EMBEDDING_MODEL"] = "Qwen/Qwen3-Embedding-8B"
os.environ["OPENAI_VECTOR_SIZE"] = "4096"
os.environ["PYTHONUNBUFFERED"] = "1"

print("Starting MCP Protocol Test...", file=sys.stderr, flush=True)

try:
    from mcp_server_qdrant.server import mcp
    print(f"✓ Server initialized: {type(mcp).__name__}", file=sys.stderr, flush=True)
    
    # Check if tools are registered
    print(f"✓ Server name: {mcp.name}", file=sys.stderr, flush=True)
    
    # Try to list tools
    if hasattr(mcp, '_tools'):
        print(f"✓ Tools registered: {len(mcp._tools)}", file=sys.stderr, flush=True)
        for tool_name in mcp._tools:
            print(f"  - {tool_name}", file=sys.stderr, flush=True)
    else:
        print("✗ No _tools attribute found", file=sys.stderr, flush=True)
    
    # Try to access FastMCP internals
    if hasattr(mcp, 'mcp'):
        print(f"✓ FastMCP instance: {type(mcp.mcp)}", file=sys.stderr, flush=True)
    
    print("\nServer is ready. Press Ctrl+C to stop.", file=sys.stderr, flush=True)
    print("=" * 60, file=sys.stderr, flush=True)
    
    # Simulate init request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        }
    }
    
    print("\nSending initialize request...", file=sys.stderr, flush=True)
    print(json.dumps(init_request), flush=True)  # This goes to stdout for MCP
    
    # Wait for response (this would normally come from stdin)
    print("\nWaiting for response...", file=sys.stderr, flush=True)
    
except Exception as e:
    print(f"\n✗ Error: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

