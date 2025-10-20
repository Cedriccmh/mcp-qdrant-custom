#!/usr/bin/env python3
"""
End-to-end test of qdrant-find/qdrant-store using FastEmbed and in-memory Qdrant.
This avoids external API calls and verifies the MCP tool layer directly.
"""
import asyncio
import os

# Configure offline, in-memory setup
os.environ["QDRANT_URL"] = ":memory:"
os.environ["COLLECTION_NAME"] = "test-ci"
os.environ["EMBEDDING_PROVIDER"] = "fastembed"
os.environ["FASTEMBED_MODEL"] = "sentence-transformers/all-MiniLM-L6-v2"
os.environ["QDRANT_SEARCH_LIMIT"] = "10"

from mcp_server_qdrant.server import mcp


async def main():
    print("=" * 80)
    print("TESTING MCP TOOLS WITH FASTEMBED (IN-MEMORY)")
    print("=" * 80)

    # List tools
    tools = await mcp.get_tools()
    print("\nTools:")
    for t in tools:
        print(f" - {t.name}")

    # 1) Find on empty collection (should return a non-empty list with 'No results...')
    print("\n1) Calling qdrant-find on empty collection...")
    res1 = await mcp.call_tool("qdrant-find", {"query": "sanity"})
    print("Result:", res1)

    # 2) Store a document
    print("\n2) Storing a sample document via qdrant-store...")
    await mcp.call_tool(
        "qdrant-store",
        {
            "information": "hello world about coding projects",
            "metadata": {"category": "test"},
        },
    )
    print("Stored.")

    # 3) Find again; should now return results list with entries
    print("\n3) Calling qdrant-find after store...")
    res2 = await mcp.call_tool("qdrant-find", {"query": "coding"})
    print("Result:", res2)

    print("\nDONE")


if __name__ == "__main__":
    asyncio.run(main())


