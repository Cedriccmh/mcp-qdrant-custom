#!/usr/bin/env python3
"""
Verify that qdrant-find now returns results with persistent storage
"""
import asyncio
import os

# Use the SAME configuration as the running server
os.environ["QDRANT_LOCAL_PATH"] = "./qdrant_data"
os.environ["COLLECTION_NAME"] = "my-memories"
os.environ["EMBEDDING_PROVIDER"] = "openai_compatible"
os.environ["OPENAI_API_KEY"] = "sk-jdunbqgibzuvmglufzuluzkqxbmxtoxburabdusipasieufv"
os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"
os.environ["EMBEDDING_MODEL"] = "Qwen/Qwen3-Embedding-8B"
os.environ["OPENAI_VECTOR_SIZE"] = "4096"

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
    print("VERIFYING QDRANT-FIND NOW WORKS")
    print("=" * 80)
    
    # Initialize server with persistent storage
    print("\n1. Initializing server with persistent storage...")
    server = QdrantMCPServer(
        tool_settings=ToolSettings(),
        qdrant_settings=QdrantSettings(),
        embedding_provider_settings=EmbeddingProviderSettings(),
    )
    
    # Check collection status
    print(f"\n2. Checking collection status...")
    collection_exists = await server.qdrant_connector._client.collection_exists("my-memories")
    print(f"   Collection exists: {collection_exists}")
    
    if collection_exists:
        info = await server.qdrant_connector._client.get_collection("my-memories")
        print(f"   Points count: {info.points_count}")
    
    # Test the queries that failed before
    test_queries = [
        "test query",
        "coding projects",
        "user preferences",
    ]
    
    ctx = MockContext()
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i + 2}. Testing query: '{query}'")
        
        results = await server.qdrant_connector.search(
            query,
            collection_name="my-memories",
            limit=3
        )
        
        if results:
            print(f"   [OK] Found {len(results)} results!")
            for j, entry in enumerate(results, 1):
                print(f"      {j}. {entry.content[:70]}...")
        else:
            print(f"   [X] No results found")
    
    print("\n" + "=" * 80)
    print("VERIFICATION COMPLETE")
    print("=" * 80)
    print("\nThe qdrant-find tool should now work in Cursor!")
    print("Try asking: 'Use qdrant-find to search for coding projects'")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())

