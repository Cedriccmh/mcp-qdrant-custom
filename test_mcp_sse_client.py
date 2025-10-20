#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test MCP server via SSE transport"""
import asyncio
import sys
import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

async def test_sse_connection():
    """Test the MCP server over SSE transport"""
    print("=" * 80)
    print("TESTING MCP SERVER VIA SSE")
    print("=" * 80)
    
    try:
        # Connect to SSE endpoint
        print("\n1. Connecting to SSE endpoint at http://localhost:8765/sse...")
        
        async with sse_client("http://localhost:8765/sse") as (read, write):
            async with ClientSession(read, write) as session:
                    
                    print("   ✓ Connected successfully!")
                    
                    # Initialize the session
                    print("\n2. Initializing MCP session...")
                    await session.initialize()
                    print("   ✓ Session initialized!")
                    
                    # List available tools
                    print("\n3. Listing available tools...")
                    tools = await session.list_tools()
                    print(f"   Found {len(tools.tools)} tools:")
                    for tool in tools.tools:
                        print(f"   - {tool.name}: {tool.description[:60]}...")
                    
                    # Test qdrant-find tool
                    print("\n4. Testing qdrant-find tool with query 'test'...")
                    result = await session.call_tool("qdrant-find", arguments={"query": "test"})
                    print(f"   Response type: {type(result)}")
                    print(f"   Content length: {len(result.content) if hasattr(result, 'content') else 'N/A'}")
                    
                    if hasattr(result, 'content') and result.content:
                        print(f"\n   Response content:")
                        for item in result.content:
                            if hasattr(item, 'text'):
                                print(f"   {item.text[:200]}...")
                            else:
                                print(f"   {item}")
                    else:
                        print(f"   [WARNING] No content in response!")
                        print(f"   Full result: {result}")
                    
                    # Test with a different query
                    print("\n5. Testing qdrant-find with query 'memory'...")
                    result2 = await session.call_tool("qdrant-find", arguments={"query": "memory"})
                    if hasattr(result2, 'content') and result2.content:
                        print(f"   Found {len(result2.content)} items")
                        for item in result2.content:
                            if hasattr(item, 'text'):
                                print(f"   {item.text[:100]}...")
                    else:
                        print(f"   No results found")
                    
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_sse_connection())

