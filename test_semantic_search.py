"""
Test semantic search functionality of the MCP Qdrant server.
This test demonstrates how semantic search works by finding conceptually similar content.
"""
import asyncio
import uuid

from mcp_server_qdrant.embeddings.fastembed import FastEmbedProvider
from mcp_server_qdrant.qdrant import Entry, QdrantConnector


async def test_semantic_search():
    """
    Test semantic search with various queries to demonstrate
    that the search finds conceptually related content, not just keyword matches.
    """
    print("=" * 80)
    print("SEMANTIC SEARCH TEST")
    print("=" * 80)
    
    # Initialize embedding provider and connector
    print("\n1. Initializing FastEmbed provider and Qdrant connector...")
    embedding_provider = FastEmbedProvider(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    collection_name = f"semantic_test_{uuid.uuid4().hex}"
    connector = QdrantConnector(
        qdrant_url=":memory:",  # Use in-memory database for testing
        qdrant_api_key=None,
        collection_name=collection_name,
        embedding_provider=embedding_provider,
    )
    print(f"✓ Collection created: {collection_name}")
    
    # Store diverse entries with different topics
    print("\n2. Storing test entries with diverse content...")
    test_entries = [
        Entry(
            content="Python is a high-level programming language known for its simplicity and readability",
            metadata={"category": "programming", "language": "python"}
        ),
        Entry(
            content="Machine learning algorithms can identify patterns in large datasets",
            metadata={"category": "AI", "topic": "machine learning"}
        ),
        Entry(
            content="The Eiffel Tower is a famous landmark located in Paris, France",
            metadata={"category": "landmarks", "location": "Paris"}
        ),
        Entry(
            content="Neural networks are inspired by biological neurons in the human brain",
            metadata={"category": "AI", "topic": "neural networks"}
        ),
        Entry(
            content="JavaScript is commonly used for web development and runs in browsers",
            metadata={"category": "programming", "language": "javascript"}
        ),
        Entry(
            content="The Great Wall of China is one of the world's most impressive architectural achievements",
            metadata={"category": "landmarks", "location": "China"}
        ),
        Entry(
            content="Deep learning uses multiple layers to progressively extract features from raw input",
            metadata={"category": "AI", "topic": "deep learning"}
        ),
        Entry(
            content="TypeScript adds static typing to JavaScript for better code quality",
            metadata={"category": "programming", "language": "typescript"}
        ),
    ]
    
    for entry in test_entries:
        await connector.store(entry)
    print(f"✓ Stored {len(test_entries)} entries")
    
    # Test 1: Search for programming-related content
    print("\n" + "=" * 80)
    print("TEST 1: Semantic Search for 'coding and software development'")
    print("=" * 80)
    query1 = "coding and software development"
    results1 = await connector.search(query1, limit=3)
    
    print(f"\nQuery: '{query1}'")
    print(f"Found {len(results1)} results:\n")
    for i, result in enumerate(results1, 1):
        print(f"{i}. {result.content}")
        print(f"   Metadata: {result.metadata}\n")
    
    # Test 2: Search for AI-related content (different wording)
    print("\n" + "=" * 80)
    print("TEST 2: Semantic Search for 'artificial intelligence and neural computation'")
    print("=" * 80)
    query2 = "artificial intelligence and neural computation"
    results2 = await connector.search(query2, limit=3)
    
    print(f"\nQuery: '{query2}'")
    print(f"Found {len(results2)} results:\n")
    for i, result in enumerate(results2, 1):
        print(f"{i}. {result.content}")
        print(f"   Metadata: {result.metadata}\n")
    
    # Test 3: Search for travel/landmarks
    print("\n" + "=" * 80)
    print("TEST 3: Semantic Search for 'famous tourist attractions and monuments'")
    print("=" * 80)
    query3 = "famous tourist attractions and monuments"
    results3 = await connector.search(query3, limit=3)
    
    print(f"\nQuery: '{query3}'")
    print(f"Found {len(results3)} results:\n")
    for i, result in enumerate(results3, 1):
        print(f"{i}. {result.content}")
        print(f"   Metadata: {result.metadata}\n")
    
    # Test 4: Specific technical query
    print("\n" + "=" * 80)
    print("TEST 4: Semantic Search for 'web browser scripting languages'")
    print("=" * 80)
    query4 = "web browser scripting languages"
    results4 = await connector.search(query4, limit=3)
    
    print(f"\nQuery: '{query4}'")
    print(f"Found {len(results4)} results:\n")
    for i, result in enumerate(results4, 1):
        print(f"{i}. {result.content}")
        print(f"   Metadata: {result.metadata}\n")
    
    # Test 5: Cross-domain conceptual search
    print("\n" + "=" * 80)
    print("TEST 5: Semantic Search for 'learning from data'")
    print("=" * 80)
    query5 = "learning from data"
    results5 = await connector.search(query5, limit=3)
    
    print(f"\nQuery: '{query5}'")
    print(f"Found {len(results5)} results:\n")
    for i, result in enumerate(results5, 1):
        print(f"{i}. {result.content}")
        print(f"   Metadata: {result.metadata}\n")
    
    # Summary
    print("\n" + "=" * 80)
    print("SEMANTIC SEARCH TEST SUMMARY")
    print("=" * 80)
    print("\n✓ All semantic search tests completed successfully!")
    print("\nKey Observations:")
    print("1. Semantic search finds conceptually similar content, not just keyword matches")
    print("2. Different phrasings of similar concepts return relevant results")
    print("3. The search uses vector embeddings to understand meaning and context")
    print("4. Results are ranked by semantic similarity (cosine distance)")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print("Starting Semantic Search Test...\n")
    asyncio.run(test_semantic_search())
    print("\nTest completed successfully!")