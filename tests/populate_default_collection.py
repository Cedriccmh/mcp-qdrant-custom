#!/usr/bin/env python3
"""
Populate the default collection with test data
This uses the same configuration as the running server
"""
import asyncio
import os

# Load configuration from .env file
from dotenv import load_dotenv
load_dotenv()

from mcp_server_qdrant.qdrant import Entry, QdrantConnector
from mcp_server_qdrant.settings import QdrantSettings, EmbeddingProviderSettings
from mcp_server_qdrant.embeddings.factory import create_embedding_provider

async def main():
    print("=" * 80)
    print("POPULATING DEFAULT COLLECTION WITH TEST DATA")
    print("=" * 80)
    
    # Initialize connector with same settings as server
    print("\n1. Initializing Qdrant connector...")
    qdrant_settings = QdrantSettings()
    embedding_settings = EmbeddingProviderSettings()
    
    # Get collection name from settings
    collection_name = qdrant_settings.collection_name
    if not collection_name:
        print("ERROR: COLLECTION_NAME is not set in .env file")
        return
    
    embedding_provider = create_embedding_provider(embedding_settings)
    connector = QdrantConnector(
        qdrant_settings.location,
        qdrant_settings.api_key,
        collection_name,
        embedding_provider,
        qdrant_settings.local_path,
    )
    
    # Check collection status
    collection_exists = await connector._client.collection_exists(collection_name)
    print(f"   Collection '{collection_name}' exists: {collection_exists}")
    
    if collection_exists:
        info = await connector._client.get_collection(collection_name)
        print(f"   Current points count: {info.points_count}")
    
    # Store test data
    print("\n2. Storing test data...")
    test_data = [
        {
            "content": "Python is a high-level programming language known for its simplicity and readability.",
            "metadata": {"category": "programming", "language": "Python"}
        },
        {
            "content": "JavaScript is the language of the web, enabling interactive websites and web applications.",
            "metadata": {"category": "programming", "language": "JavaScript"}
        },
        {
            "content": "Machine learning is a subset of artificial intelligence focused on learning from data.",
            "metadata": {"category": "AI", "topic": "machine learning"}
        },
        {
            "content": "Qdrant is a vector database designed for similarity search and AI applications.",
            "metadata": {"category": "database", "type": "vector"}
        },
        {
            "content": "The MCP protocol enables seamless integration between AI assistants and external tools.",
            "metadata": {"category": "protocol", "type": "MCP"}
        }
    ]
    
    for i, data in enumerate(test_data, 1):
        entry = Entry(content=data["content"], metadata=data["metadata"])
        await connector.store(entry, collection_name=collection_name)
        print(f"   {i}. Stored: {data['content'][:65]}...")
    
    print(f"\n[OK] Stored {len(test_data)} entries successfully")
    
    # Verify data was stored
    print("\n3. Verifying data storage...")
    collection_info = await connector._client.get_collection(collection_name)
    print(f"   Total points in collection: {collection_info.points_count}")
    
    # Test a search
    print("\n4. Testing semantic search...")
    test_query = "programming languages"
    results = await connector.search(test_query, collection_name=collection_name, limit=3)
    
    if results:
        print(f"   [OK] Found {len(results)} results for '{test_query}':")
        for i, entry in enumerate(results, 1):
            print(f"      {i}. {entry.content[:60]}...")
    else:
        print(f"   [X] No results found")
    
    print("\n" + "=" * 80)
    print("DATA POPULATION COMPLETE")
    print("=" * 80)
    print(f"\nThe '{collection_name}' collection now has test data.")
    print("You can now test the mcp_qdrant_qdrant-find tool in Cursor!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())

