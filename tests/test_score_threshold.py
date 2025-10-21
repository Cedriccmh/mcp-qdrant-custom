"""
Test script for the score threshold feature.
This script verifies that the score threshold configuration works correctly.
"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

from mcp_server_qdrant.settings import QdrantSettings, EmbeddingProviderSettings
from mcp_server_qdrant.embeddings.factory import create_embedding_provider
from mcp_server_qdrant.qdrant import QdrantConnector, Entry

# Load .env file
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"[OK] Loaded environment from {env_path}")
else:
    print("[WARN] No .env file found, using system environment variables")


async def test_score_threshold():
    """Test the score threshold functionality."""
    
    print("\n" + "="*60)
    print("SCORE THRESHOLD FEATURE TEST")
    print("="*60)
    
    # Load settings from environment
    qdrant_settings = QdrantSettings()
    embedding_settings = EmbeddingProviderSettings()
    
    print(f"\nConfiguration:")
    print(f"  Qdrant URL: {qdrant_settings.location}")
    print(f"  Collection: {qdrant_settings.collection_name}")
    print(f"  Search Limit: {qdrant_settings.search_limit}")
    print(f"  Score Threshold: {qdrant_settings.score_threshold}")
    print(f"  Embedding Provider: {embedding_settings.provider_type}")
    print(f"  Embedding Model: {embedding_settings.model_name}")
    
    # Create embedding provider
    print(f"\n[*] Creating embedding provider...")
    embedding_provider = create_embedding_provider(embedding_settings)
    
    # Create connector
    print(f"[*] Creating Qdrant connector...")
    connector = QdrantConnector(
        qdrant_url=qdrant_settings.location,
        qdrant_api_key=qdrant_settings.api_key,
        collection_name=qdrant_settings.collection_name,
        embedding_provider=embedding_provider,
        qdrant_local_path=qdrant_settings.local_path,
        score_threshold=qdrant_settings.score_threshold,
    )
    
    # Check if collection exists
    collections = await connector.get_collection_names()
    print(f"\n[*] Available collections: {collections}")
    
    if qdrant_settings.collection_name not in collections:
        print(f"\n[WARN] Warning: Collection '{qdrant_settings.collection_name}' does not exist.")
        print(f"  Creating it with some sample data for testing...")
        
        # Store some test data
        test_entries = [
            Entry(content="Machine learning is a subset of artificial intelligence", metadata={"topic": "ML"}),
            Entry(content="Deep learning uses neural networks with multiple layers", metadata={"topic": "DL"}),
            Entry(content="Python is a popular programming language", metadata={"topic": "Programming"}),
            Entry(content="Data science involves analyzing and interpreting data", metadata={"topic": "Data"}),
        ]
        
        for i, entry in enumerate(test_entries, 1):
            await connector.store(entry, collection_name=qdrant_settings.collection_name)
            print(f"  [OK] Stored test entry {i}/{len(test_entries)}")
    
    # Test search without threshold override
    print(f"\n" + "-"*60)
    print("TEST 1: Search with default threshold from settings")
    print("-"*60)
    
    test_query = "artificial intelligence and neural networks"
    print(f"Query: '{test_query}'")
    
    results = await connector.search(
        query=test_query,
        collection_name=qdrant_settings.collection_name,
        limit=qdrant_settings.search_limit,
    )
    
    print(f"\nResults: {len(results)} entries found")
    for i, result in enumerate(results, 1):
        print(f"\n  [{i}] Score: {result.score:.4f}" if result.score else f"\n  [{i}] Score: N/A")
        print(f"      Content: {result.content[:80]}..." if len(result.content) > 80 else f"      Content: {result.content}")
        if result.metadata:
            print(f"      Metadata: {result.metadata}")
    
    # Test search with specific threshold (0.5)
    print(f"\n" + "-"*60)
    print("TEST 2: Search with threshold=0.5 (override)")
    print("-"*60)
    
    results_threshold = await connector.search(
        query=test_query,
        collection_name=qdrant_settings.collection_name,
        limit=qdrant_settings.search_limit,
        score_threshold=0.5,
    )
    
    print(f"\nResults: {len(results_threshold)} entries found (filtered by score >= 0.5)")
    for i, result in enumerate(results_threshold, 1):
        print(f"\n  [{i}] Score: {result.score:.4f}" if result.score else f"\n  [{i}] Score: N/A")
        print(f"      Content: {result.content[:80]}..." if len(result.content) > 80 else f"      Content: {result.content}")
        if result.metadata:
            print(f"      Metadata: {result.metadata}")
    
    # Test search with strict threshold (0.8)
    print(f"\n" + "-"*60)
    print("TEST 3: Search with threshold=0.8 (strict)")
    print("-"*60)
    
    results_strict = await connector.search(
        query=test_query,
        collection_name=qdrant_settings.collection_name,
        limit=qdrant_settings.search_limit,
        score_threshold=0.8,
    )
    
    print(f"\nResults: {len(results_strict)} entries found (filtered by score >= 0.8)")
    for i, result in enumerate(results_strict, 1):
        print(f"\n  [{i}] Score: {result.score:.4f}" if result.score else f"\n  [{i}] Score: N/A")
        print(f"      Content: {result.content[:80]}..." if len(result.content) > 80 else f"      Content: {result.content}")
        if result.metadata:
            print(f"      Metadata: {result.metadata}")
    
    # Summary
    print(f"\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Default threshold (from settings): {qdrant_settings.score_threshold}")
    print(f"Results without filter: {len(results)}")
    print(f"Results with threshold=0.5: {len(results_threshold)}")
    print(f"Results with threshold=0.8: {len(results_strict)}")
    
    if len(results) >= len(results_threshold) >= len(results_strict):
        print(f"\n[PASS] Test PASSED: Threshold filtering works as expected!")
        print(f"       (More strict thresholds return fewer or equal results)")
    else:
        print(f"\n[FAIL] Test FAILED: Unexpected result counts")
    
    print(f"\n" + "="*60)


if __name__ == "__main__":
    try:
        asyncio.run(test_score_threshold())
    except Exception as e:
        print(f"\n[ERROR] Error during test: {e}")
        import traceback
        traceback.print_exc()

