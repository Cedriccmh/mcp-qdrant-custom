#!/usr/bin/env python3
"""Test the MCP tool call directly"""
import asyncio
import os

# Match server configuration
os.environ["QDRANT_LOCAL_PATH"] = "./qdrant_data"
os.environ["COLLECTION_NAME"] = "ws-77b2ac62ce00ae8e"
os.environ["EMBEDDING_PROVIDER"] = "openai_compatible"
os.environ["OPENAI_API_KEY"] = "sk-jdunbqgibzuvmglufzuluzkqxbmxtoxburabdusipasieufv"
os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"
os.environ["EMBEDDING_MODEL"] = "Qwen/Qwen3-Embedding-8B"
os.environ["OPENAI_VECTOR_SIZE"] = "4096"

from mcp_server_qdrant.server import mcp

class MockContext:
    """Mock context for testing"""
    async def debug(self, message: str):
        print(f"[DEBUG] {message}")

async def test_tool_call():
    print("=" * 80)
    print("TESTING MCP TOOL CALL DIRECTLY")
    print("=" * 80)
    
    # Get the tools
    print("\n1. Getting available tools...")
    tools = await mcp.get_tools()
    print(f"   Available tools: {len(tools)}")
    for tool in tools:
        print(f"   - {tool.name}: {tool.description[:60]}")
    
    # Find the qdrant-find tool
    print("\n2. Finding qdrant-find tool...")
    find_tool = None
    for tool in tools:
        if tool.name == "qdrant-find":
            find_tool = tool
            break
    
    if not find_tool:
        print("   [ERROR] qdrant-find tool not found!")
        return
    
    print(f"   [OK] Found tool: {find_tool.name}")
    print(f"   Description: {find_tool.description}")
    print(f"   Input schema: {find_tool.inputSchema}")
    
    # Call the tool
    print("\n3. Calling qdrant-find tool with query 'programming languages'...")
    try:
        result = await mcp.call_tool(
            "qdrant-find",
            {"query": "programming languages"}
        )
        print(f"   [OK] Tool call succeeded!")
        print(f"   Result type: {type(result)}")
        print(f"   Result: {result}")
        
        # Check if result is a list
        if isinstance(result, list):
            print(f"\n   Result is a list with {len(result)} items:")
            for i, item in enumerate(result, 1):
                print(f"      {i}. {item}")
        
    except Exception as e:
        print(f"   [ERROR] Tool call failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test with no results scenario
    print("\n4. Testing with unlikely query...")
    try:
        result = await mcp.call_tool(
            "qdrant-find",
            {"query": "quantum entanglement and warp drives"}
        )
        print(f"   Result: {result}")
        print(f"   Result type: {type(result)}")
        
    except Exception as e:
        print(f"   [ERROR] Tool call failed: {e}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    asyncio.run(test_tool_call())

