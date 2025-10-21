#!/usr/bin/env python3
"""快速测试脚本 - 验证服务器能否正常初始化"""
import os
import sys

# Load configuration from .env file
from dotenv import load_dotenv
load_dotenv()

print("=" * 60, file=sys.stderr)
print("Quick Test - MCP Server Initialization", file=sys.stderr)
print("=" * 60, file=sys.stderr)
print("Configuration loaded from .env file", file=sys.stderr)
print("", file=sys.stderr)

try:
    print("\n[1/3] Importing server module...", file=sys.stderr)
    from mcp_server_qdrant.server import mcp
    print("✓ Server module imported successfully", file=sys.stderr)
    
    print("\n[2/3] Checking server configuration...", file=sys.stderr)
    print(f"  - Embedding provider: {mcp.embedding_provider.__class__.__name__}", file=sys.stderr)
    print(f"  - Vector size: {mcp.embedding_provider.get_vector_size()}", file=sys.stderr)
    print(f"  - Collection: {mcp.qdrant_settings.collection_name}", file=sys.stderr)
    print(f"  - Qdrant URL: {mcp.qdrant_settings.location}", file=sys.stderr)
    print("✓ Configuration OK", file=sys.stderr)
    
    print("\n[3/3] Testing stdio communication...", file=sys.stderr)
    print("  Server is ready for stdio communication", file=sys.stderr)
    print("  Press Ctrl+C to stop the server", file=sys.stderr)
    print("\n" + "=" * 60, file=sys.stderr)
    print("Starting server in stdio mode...\n", file=sys.stderr)
    
    # Run the server
    mcp.run(transport="stdio")
    
except KeyboardInterrupt:
    print("\n\nServer stopped by user", file=sys.stderr)
except Exception as e:
    print(f"\n✗ Error: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)

