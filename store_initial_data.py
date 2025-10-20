#!/usr/bin/env python3
"""
Store initial test data in the MCP server's database
This will work with persistent storage (QDRANT_LOCAL_PATH)
"""
import asyncio
import os

# Use the SAME configuration as the running server
os.environ["QDRANT_LOCAL_PATH"] = "./qdrant_data"
os.environ["COLLECTION_NAME"] = "ws-77b2ac62ce00ae8e"
os.environ["EMBEDDING_PROVIDER"] = "openai_compatible"
os.environ["OPENAI_API_KEY"] = "sk-jdunbqgibzuvmglufzuluzkqxbmxtoxburabdusipasieufv"
os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"
os.environ["EMBEDDING_MODEL"] = "Qwen/Qwen3-Embedding-8B"
os.environ["OPENAI_VECTOR_SIZE"] = "4096"

from mcp_server_qdrant.qdrant import Entry, QdrantConnector
from mcp_server_qdrant.embeddings.factory import create_embedding_provider
from mcp_server_qdrant.settings import EmbeddingProviderSettings

async def main():
    print("=" * 80)
    print("STORING INITIAL TEST DATA")
    print("=" * 80)
    
    # Create embedding provider
    print("\n1. Initializing with Qwen3-Embedding-8B...")
    embedding_provider = create_embedding_provider(EmbeddingProviderSettings())
    
    # Create connector
    connector = QdrantConnector(
        qdrant_url=None,
        qdrant_api_key=None,
        collection_name="ws-77b2ac62ce00ae8e",
        embedding_provider=embedding_provider,
        qdrant_local_path="./qdrant_data"
    )
    
    # Store test data
    test_entries = [
        Entry(
            content="I am working on an MCP server project using Qdrant and Python",
            metadata={"category": "project", "tags": ["mcp", "qdrant", "python"]}
        ),
        Entry(
            content="The mcp-qdrant-custom project uses Qwen3-Embedding-8B model from SiliconFlow",
            metadata={"category": "tech", "tags": ["embedding", "ai"]}
        ),
        Entry(
            content="User preferences: I prefer using semantic search over keyword matching",
            metadata={"category": "preferences", "type": "search"}
        ),
        Entry(
            content="This is a coding project that implements MCP protocol for vector database integration",
            metadata={"category": "project", "tags": ["coding", "mcp", "vector-db"]}
        ),
        Entry(
            content="Testing the qdrant-find tool to search through stored memories",
            metadata={"category": "test", "tool": "qdrant-find"}
        ),
    ]
    
    print(f"\n2. Storing {len(test_entries)} entries...")
    for i, entry in enumerate(test_entries, 1):
        await connector.store(entry, collection_name="ws-77b2ac62ce00ae8e")
        print(f"   [{i}] Stored: {entry.content[:60]}...")
    
    print("\n[OK] All data stored successfully!")
    
    # Verify by searching
    print("\n3. Verifying data with test search...")
    results = await connector.search(
        "coding projects",
        collection_name="ws-77b2ac62ce00ae8e",
        limit=3
    )
    
    print(f"\n   Found {len(results)} results for 'coding projects':")
    for i, entry in enumerate(results, 1):
        print(f"   {i}. {entry.content[:60]}...")
    
    print("\n" + "=" * 80)
    print("SUCCESS! Database populated and ready to use!")
    print("=" * 80)
    print("\nNow you can:")
    print("1. Restart the MCP server with: start_mcp_server.bat")
    print("2. Use qdrant-find in Cursor to search for these memories")
    print("3. Data will persist across server restarts!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())

