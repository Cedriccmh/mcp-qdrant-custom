#!/usr/bin/env python3
"""
Comprehensive comparison of mcp_qdrant_qdrant-find vs codebase_search tools
This script demonstrates the differences between the two semantic search tools
"""
import asyncio
import os

# Setup environment for Qdrant
os.environ["QDRANT_LOCAL_PATH"] = "./qdrant_data"
os.environ["COLLECTION_NAME"] = "ws-77b2ac62ce00ae8e"
os.environ["EMBEDDING_PROVIDER"] = "openai_compatible"
os.environ["OPENAI_API_KEY"] = "sk-jdunbqgibzuvmglufzuluzkqxbmxtoxburabdusipasieufv"
os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"
os.environ["EMBEDDING_MODEL"] = "Qwen/Qwen3-Embedding-8B"
os.environ["OPENAI_VECTOR_SIZE"] = "4096"

from mcp_server_qdrant.server import mcp

async def test_qdrant_find_tool():
    """Test the Qdrant find tool to see what it returns"""
    print("=" * 80)
    print("TESTING mcp_qdrant_qdrant-find TOOL")
    print("=" * 80)
    
    connector = mcp.qdrant_connector
    
    # Check collection status
    print("\n1. Checking collection status...")
    collection_name = "ws-77b2ac62ce00ae8e"
    exists = await connector._client.collection_exists(collection_name)
    print(f"   Collection '{collection_name}' exists: {exists}")
    
    if exists:
        info = await connector._client.get_collection(collection_name)
        print(f"   Points count: {info.points_count}")
    else:
        print("   [!] Collection is empty - no data to search")
        return
    
    # Test queries
    queries = [
        "semantic search implementation",
        "python programming",
        "how does vector search work",
        "embedding models and configuration"
    ]
    
    print("\n2. Testing semantic search queries...")
    for i, query in enumerate(queries, 1):
        print(f"\n   Query {i}: '{query}'")
        print("   " + "-" * 70)
        
        results = await connector.search(query, collection_name=collection_name, limit=3)
        
        if results:
            print(f"   Found {len(results)} results:")
            for j, entry in enumerate(results[:2], 1):  # Show top 2
                content_preview = entry.content[:80].replace('\n', ' ')
                score = f"{entry.score:.3f}" if entry.score else "N/A"
                file_path = entry.metadata.get("filePath", "Unknown") if entry.metadata else "Unknown"
                print(f"      {j}. Score: {score}")
                print(f"         File: {file_path}")
                print(f"         Content: {content_preview}...")
        else:
            print("   No results found")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    print("\nStarting tool comparison test...\n")
    asyncio.run(test_qdrant_find_tool())
    
    print("\n\n")
    print("=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)
    print("""
mcp_qdrant_qdrant-find vs codebase_search:

1. DATA SOURCE:
   • mcp_qdrant_qdrant-find: Persistent vector database (Qdrant)
   • codebase_search: Live files in current repository

2. SEARCH SCOPE:
   • mcp_qdrant_qdrant-find: Only what was explicitly stored
   • codebase_search: All code files in the repository

3. PERSISTENCE:
   • mcp_qdrant_qdrant-find: Data survives restarts ✅
   • codebase_search: No persistence, always fresh ✅

4. USE CASES:
   • mcp_qdrant_qdrant-find:
     - Long-term memory / knowledge base
     - User preferences and notes
     - Cross-session context
     - Project documentation
   
   • codebase_search:
     - Finding implementations in code
     - Understanding code structure
     - Navigation and exploration
     - Live code analysis

5. RESULT FORMAT:
   • mcp_qdrant_qdrant-find: Formatted text with scores and metadata
   • codebase_search: Code chunks with line numbers and citations

6. CONFIGURATION:
   • mcp_qdrant_qdrant-find: Requires Qdrant setup + embedding model
   • codebase_search: Zero configuration, always ready

7. STRENGTHS:
   • mcp_qdrant_qdrant-find:
     ✅ Cross-session memory
     ✅ Can store any text/data
     ✅ Survives code changes
     ✅ Write capability
   
   • codebase_search:
     ✅ Always up-to-date with code
     ✅ No storage needed
     ✅ Complete code context
     ✅ Better for code navigation

RECOMMENDATION: Use BOTH tools for different purposes!
- Use codebase_search for understanding existing code
- Use mcp_qdrant_qdrant-find for building persistent knowledge
""")


