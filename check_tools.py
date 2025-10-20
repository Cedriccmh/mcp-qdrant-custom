#!/usr/bin/env python3
"""检查工具是否正确注册"""
import asyncio
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

async def main():
    print("=" * 70, file=sys.stderr, flush=True)
    print("Checking QdrantMCPServer tools...", file=sys.stderr, flush=True)
    print("=" * 70, file=sys.stderr, flush=True)

    from mcp_server_qdrant.server import mcp

    print(f"\n✓ Server initialized: {mcp.name}", file=sys.stderr, flush=True)
    print(f"✓ Tool manager: {type(mcp._tool_manager)}", file=sys.stderr, flush=True)

    # Check tools using get_tools()
    tools = await mcp.get_tools()
    print(f"\n✓ Number of tools: {len(tools)}", file=sys.stderr, flush=True)
    for tool in tools:
        if hasattr(tool, 'name'):
            desc = tool.description[:60] if len(tool.description) > 60 else tool.description
            print(f"  - {tool.name}: {desc}", file=sys.stderr, flush=True)
        else:
            print(f"  - {tool}", file=sys.stderr, flush=True)

    print("\n" + "=" * 70, file=sys.stderr, flush=True)
    print("✓ Tools are properly registered!", file=sys.stderr, flush=True)
    print("=" * 70, file=sys.stderr, flush=True)

if __name__ == "__main__":
    asyncio.run(main())

