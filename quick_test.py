#!/usr/bin/env python3
"""快速测试脚本 - 验证服务器能否正常初始化"""
import os
import sys

# 设置环境变量
os.environ["QDRANT_URL"] = "http://localhost:6333"
os.environ["COLLECTION_NAME"] = "test"
os.environ["EMBEDDING_PROVIDER"] = "openai_compatible"
os.environ["OPENAI_API_KEY"] = "sk-test"
os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"
os.environ["EMBEDDING_MODEL"] = "Qwen/Qwen3-Embedding-8B"
os.environ["OPENAI_VECTOR_SIZE"] = "4096"

print("=" * 60, file=sys.stderr)
print("Quick Test - MCP Server Initialization", file=sys.stderr)
print("=" * 60, file=sys.stderr)

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

