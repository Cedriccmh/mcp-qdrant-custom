#!/usr/bin/env python3
"""Debug why qdrant search returns empty results"""
import os
import asyncio

# Set environment variables
os.environ["QDRANT_LOCAL_PATH"] = "./qdrant_data"
os.environ["COLLECTION_NAME"] = "ws-77b2ac62ce00ae8e"
os.environ["EMBEDDING_PROVIDER"] = "openai_compatible"
os.environ["OPENAI_API_KEY"] = "sk-jdunbqgibzuvmglufzuluzkqxbmxtoxburabdusipasieufv"
os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"
os.environ["EMBEDDING_MODEL"] = "Qwen/Qwen3-Embedding-8B"
os.environ["OPENAI_VECTOR_SIZE"] = "4096"

from mcp_server_qdrant.server import mcp

async def debug_search():
    print("=" * 80)
    print("DEBUGGING QDRANT SEARCH")
    print("=" * 80)
    
    # Get the server instance
    server = mcp
    
    # Access the qdrant connector
    print("\n1. Checking qdrant connector...")
    connector = server.qdrant_connector
    print(f"   Connector type: {type(connector)}")
    print(f"   Collection name: {server.qdrant_settings.collection_name}")
    
    # Check qdrant client
    print("\n2. Checking qdrant client...")
    client = connector._client
    print(f"   Client type: {type(client)}")
    
    # List collections
    print("\n3. Listing collections...")
    collections = await client.get_collections()
    print(f"   Collections: {[c.name for c in collections.collections]}")
    
    # Check collection info
    collection_name = server.qdrant_settings.collection_name
    print(f"\n4. Checking collection '{collection_name}'...")
    try:
        info = await client.get_collection(collection_name)
        print(f"   Points count: {info.points_count}")
        print(f"   Config: {info.config.params}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # Try to scroll some points
    print(f"\n5. Fetching some points from '{collection_name}'...")
    try:
        scroll_result = await client.scroll(
            collection_name=collection_name,
            limit=3,
            with_payload=True,
            with_vectors=False
        )
        points = scroll_result[0]
        print(f"   Found {len(points)} points:")
        for point in points:
            print(f"   - ID: {point.id}")
            print(f"     Payload: {point.payload}")
    except Exception as e:
        print(f"   [ERROR] {e}")
        import traceback
        traceback.print_exc()
    
    # Try direct search
    print(f"\n6. Testing direct search with embedding...")
    try:
        # Get embedding for query
        query = "test"
        print(f"   Query: '{query}'")
        
        # Try the search method
        print(f"\n   Calling connector.search()...")
        results = await connector.search(
            query=query,
            collection_name=collection_name,
            limit=5
        )
        print(f"   Results: {len(results)} entries")
        for entry in results:
            print(f"   - {entry}")
    except Exception as e:
        print(f"   [ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("DEBUG COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(debug_search())

