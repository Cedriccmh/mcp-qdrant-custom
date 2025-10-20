#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detailed test of the qdrant-find tool"""
import asyncio
import sys
from mcp import ClientSession
from mcp.client.sse import sse_client

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

async def test_tool():
    print("=" * 80)
    print("DETAILED QDRANT-FIND TOOL TEST")
    print("=" * 80)
    
    async with sse_client("http://localhost:8765/sse") as (read, write):
        async with ClientSession(read, write) as session:
            
            # Initialize session
            print("\n1. Initializing session...")
            await session.initialize()
            
            # Test 1: Basic query
            print("\n2. Testing query: 'python programming'")
            result = await session.call_tool("qdrant-find", arguments={"query": "python programming"})
            print(f"   Result type: {type(result)}")
            print(f"   Result: {result}")
            print(f"   Is Error: {result.isError}")
            print(f"   Content: {result.content}")
            print(f"   Content type: {type(result.content)}")
            print(f"   Content length: {len(result.content)}")
            
            if result.content:
                print("\n   Content items:")
                for i, item in enumerate(result.content):
                    print(f"   [{i}] Type: {type(item)}")
                    print(f"       Value: {item}")
                    if hasattr(item, '__dict__'):
                        print(f"       Attributes: {item.__dict__}")
            
            # Test 2: Another query
            print("\n3. Testing query: 'docker containers'")
            result2 = await session.call_tool("qdrant-find", arguments={"query": "docker containers"})
            print(f"   Content length: {len(result2.content)}")
            if result2.content:
                for item in result2.content:
                    if hasattr(item, 'text'):
                        print(f"   {item.text[:150]}")
                    else:
                        print(f"   {str(item)[:150]}")
            
            # Test 3: Query that should find nothing
            print("\n4. Testing query that should match nothing: 'xyz123abc'")
            result3 = await session.call_tool("qdrant-find", arguments={"query": "xyz123abc"})
            print(f"   Content length: {len(result3.content)}")
            if result3.content:
                for item in result3.content:
                    print(f"   {item}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_tool())


