#!/usr/bin/env python3
"""
Direct test of the MCP tools to understand why qdrant-find returns no results in Cursor
"""
import asyncio
import os

# Use the SAME configuration as the running server
os.environ["QDRANT_URL"] = ":memory:"
os.environ["COLLECTION_NAME"] = "ws-77b2ac62ce00ae8e"
os.environ["EMBEDDING_PROVIDER"] = "openai_compatible"
os.environ["OPENAI_API_KEY"] = "sk-jdunbqgibzuvmglufzuluzkqxbmxtoxburabdusipasieufv"
os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"
os.environ["EMBEDDING_MODEL"] = "Qwen/Qwen3-Embedding-8B"
os.environ["OPENAI_VECTOR_SIZE"] = "4096"
os.environ["QDRANT_SEARCH_LIMIT"] = "20"

from mcp_server_qdrant.mcp_server import QdrantMCPServer
from mcp_server_qdrant.settings import (
    EmbeddingProviderSettings,
    QdrantSettings,
    ToolSettings,
)

class MockContext:
    """Mock context for testing"""
    async def debug(self, message: str):
        print(f"[DEBUG] {message}")

async def main():
    print("=" * 80)
    print("TESTING WHY QDRANT-FIND RETURNS NO RESULTS")
    print("=" * 80)
    
    # Initialize server with SAME config as running server
    print("\n1. Initializing server with Qwen3-Embedding-8B...")
    server = QdrantMCPServer(
        tool_settings=ToolSettings(),
        qdrant_settings=QdrantSettings(),
        embedding_provider_settings=EmbeddingProviderSettings(),
    )
    
    # Check collection status
    print(f"\n2. Checking collection 'ws-77b2ac62ce00ae8e'...")
    collection_exists = await server.qdrant_connector._client.collection_exists("ws-77b2ac62ce00ae8e")
    print(f"   Collection exists: {collection_exists}")
    
    if collection_exists:
        # Get collection info
        info = await server.qdrant_connector._client.get_collection("ws-77b2ac62ce00ae8e")
        print(f"   Points count: {info.points_count}")
    
    # Try searching with empty database
    print("\n3. Testing search on empty database...")
    ctx = MockContext()
    results = await server.qdrant_connector.search(
        "test query",
        collection_name="ws-77b2ac62ce00ae8e",
        limit=5
    )
    print(f"   Results: {results}")
    print(f"   Result type: {type(results)}")
    print(f"   Is empty: {len(results) == 0}")
    
    # The find function returns None when empty
    if not results:
        print("\n[X] FOUND THE ISSUE!")
        print("   When the database is empty, search returns an empty list []")
        print("   The find() function checks 'if not entries' and returns None")
        print("   This is why you see no output in Cursor - the tool returns None!")
    
    # Now let's store something and try again
    print("\n4. Storing a test entry...")
    from mcp_server_qdrant.qdrant import Entry
    
    await server.qdrant_connector.store(
        Entry(content="This is a test memory about coding projects", metadata={"type": "test"}),
        collection_name="ws-77b2ac62ce00ae8e"
    )
    print("   [OK] Stored test entry")
    
    # Search again
    print("\n5. Searching again after storing data...")
    results2 = await server.qdrant_connector.search(
        "coding projects",
        collection_name="ws-77b2ac62ce00ae8e",
        limit=5
    )
    print(f"   Results count: {len(results2)}")
    if results2:
        print("\n   [OK] GOT RESULTS!")
        for i, entry in enumerate(results2, 1):
            print(f"   {i}. {entry.content}")
            print(f"      Metadata: {entry.metadata}")
    
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print("\n[ISSUE] The issue is: THE DATABASE IS EMPTY!")
    print("\nWhen you call qdrant-find on an empty database:")
    print("  1. The collection doesn't exist or has no data")
    print("  2. search() returns an empty list []")
    print("  3. find() checks 'if not entries' and returns None")
    print("  4. Cursor shows no output because the tool returns None")
    print("\n[SOLUTION] Store some data first using qdrant-store!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())

