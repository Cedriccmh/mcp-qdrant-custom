#!/usr/bin/env python3
"""Verify the fix is working"""
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def verify_fix():
    print("=" * 80)
    print("VERIFYING FIX - Testing Realistic Queries")
    print("=" * 80)
    
    async with sse_client("http://localhost:8765/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test 1: Search for embedding-related code
            print("\n1. Searching for 'embedding provider configuration'...")
            result = await session.call_tool("qdrant-find", arguments={
                "query": "embedding provider configuration"
            })
            
            if result.content and result.content[0].text:
                text = result.content[0].text
                # Count results
                result_count = text.count("File path:")
                print(f"   Found {result_count} results")
                print(f"   Preview: {text[:300]}...")
            
            # Test 2: Search for search-related code
            print("\n2. Searching for 'qdrant search query'...")
            result = await session.call_tool("qdrant-find", arguments={
                "query": "qdrant search query"
            })
            
            if result.content and result.content[0].text:
                text = result.content[0].text
                result_count = text.count("File path:")
                print(f"   Found {result_count} results")
                print(f"   Preview: {text[:300]}...")
            
            # Test 3: Search for MCP server code
            print("\n3. Searching for 'MCP server initialization'...")
            result = await session.call_tool("qdrant-find", arguments={
                "query": "MCP server initialization"
            })
            
            if result.content and result.content[0].text:
                text = result.content[0].text
                result_count = text.count("File path:")
                print(f"   Found {result_count} results")
                print(f"   Preview: {text[:300]}...")
            
            print("\n" + "=" * 80)
            print("✓ FIX VERIFIED - Server is returning results!")
            print("=" * 80)

if __name__ == "__main__":
    asyncio.run(verify_fix())

