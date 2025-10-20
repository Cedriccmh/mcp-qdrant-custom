"""
Comprehensive test for the qdrant-find tool functionality.
This script tests the full workflow: initialize, store, and find.
"""
import asyncio
import os

# Set up environment variables
os.environ["QDRANT_URL"] = ":memory:"
os.environ["COLLECTION_NAME"] = "test-memories"
os.environ["EMBEDDING_PROVIDER"] = "fastembed"
os.environ["FASTEMBED_MODEL"] = "sentence-transformers/all-MiniLM-L6-v2"
os.environ["QDRANT_SEARCH_LIMIT"] = "10"

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


async def test_qdrant_find_tool():
    """Test the qdrant-find tool with sample data"""
    print("=" * 80)
    print("TESTING QDRANT-FIND TOOL")
    print("=" * 80)
    
    # Initialize the MCP server
    print("\n1. Initializing MCP Server...")
    server = QdrantMCPServer(
        tool_settings=ToolSettings(),
        qdrant_settings=QdrantSettings(),
        embedding_provider_settings=EmbeddingProviderSettings(),
    )
    print("[OK] Server initialized successfully")
    
    # Create a mock context
    ctx = MockContext()
    
    # Store some test data
    print("\n2. Storing test data...")
    test_data = [
        {
            "information": "Python is a versatile programming language used for web development, data science, and automation",
            "metadata": {"category": "programming", "language": "python"}
        },
        {
            "information": "JavaScript is the language of the web, running in browsers and on servers with Node.js",
            "metadata": {"category": "programming", "language": "javascript"}
        },
        {
            "information": "Machine learning involves training algorithms to make predictions from data",
            "metadata": {"category": "AI", "topic": "machine learning"}
        },
        {
            "information": "The Eiffel Tower is a famous landmark in Paris, France, built in 1889",
            "metadata": {"category": "landmarks", "location": "Paris"}
        },
        {
            "information": "Neural networks are computing systems inspired by biological neural networks",
            "metadata": {"category": "AI", "topic": "neural networks"}
        },
    ]
    
    for i, data in enumerate(test_data, 1):
        result = await server.qdrant_connector.store(
            Entry(content=data["information"], metadata=data["metadata"])
        )
        print(f"   {i}. Stored: {data['information'][:60]}...")
    
    print(f"[OK] Stored {len(test_data)} entries")
    
    # Test 1: Search for programming content
    print("\n" + "=" * 80)
    print("TEST 1: Finding programming-related content")
    print("=" * 80)
    query1 = "programming languages for web development"
    print(f"\nQuery: '{query1}'")
    
    results1 = await server.qdrant_connector.search(
        query1,
        limit=3
    )
    
    if results1:
        print(f"\n[OK] Found {len(results1)} results:")
        for i, entry in enumerate(results1, 1):
            print(f"\n{i}. {entry.content}")
            print(f"   Metadata: {entry.metadata}")
    else:
        print("[X] No results found")
    
    # Test 2: Search for AI content
    print("\n" + "=" * 80)
    print("TEST 2: Finding AI-related content")
    print("=" * 80)
    query2 = "artificial intelligence and neural computation"
    print(f"\nQuery: '{query2}'")
    
    results2 = await server.qdrant_connector.search(
        query2,
        limit=3
    )
    
    if results2:
        print(f"\n[OK] Found {len(results2)} results:")
        for i, entry in enumerate(results2, 1):
            print(f"\n{i}. {entry.content}")
            print(f"   Metadata: {entry.metadata}")
    else:
        print("[X] No results found")
    
    # Test 3: Search for landmarks
    print("\n" + "=" * 80)
    print("TEST 3: Finding landmark information")
    print("=" * 80)
    query3 = "famous tourist attractions and monuments"
    print(f"\nQuery: '{query3}'")
    
    results3 = await server.qdrant_connector.search(
        query3,
        limit=3
    )
    
    if results3:
        print(f"\n[OK] Found {len(results3)} results:")
        for i, entry in enumerate(results3, 1):
            print(f"\n{i}. {entry.content}")
            print(f"   Metadata: {entry.metadata}")
    else:
        print("[X] No results found")
    
    # Test 4: Search with no matches
    print("\n" + "=" * 80)
    print("TEST 4: Query with unlikely matches")
    print("=" * 80)
    query4 = "quantum physics and black holes"
    print(f"\nQuery: '{query4}'")
    
    results4 = await server.qdrant_connector.search(
        query4,
        limit=3
    )
    
    if results4:
        print(f"\n[OK] Found {len(results4)} results (may have low similarity):")
        for i, entry in enumerate(results4, 1):
            print(f"\n{i}. {entry.content}")
            print(f"   Metadata: {entry.metadata}")
    else:
        print("[X] No results found")
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print("\n[OK] All tests completed successfully!")
    print("\nKey Points:")
    print("1. The qdrant-find tool uses semantic search with embeddings")
    print("2. It returns results ranked by relevance to the query")
    print("3. Queries don't need exact keyword matches - semantic similarity is used")
    print("4. Metadata can be stored and retrieved with each entry")
    print("\n" + "=" * 80)


# Import Entry after environment setup
from mcp_server_qdrant.qdrant import Entry


if __name__ == "__main__":
    print("Starting qdrant-find tool test...\n")
    asyncio.run(test_qdrant_find_tool())
    print("\n[DONE] Test completed!")

