"""
Test script to verify the new response format for qdrant-find tool.
This directly tests the format_entry method to show what the new format looks like.
"""
import json
import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp_server_qdrant.mcp_server import QdrantMCPServer
from mcp_server_qdrant.qdrant import Entry
from mcp_server_qdrant.settings import QdrantSettings, EmbeddingProviderSettings, ToolSettings


def test_format_entry():
    """Test the new format_entry method"""
    print("=" * 80)
    print("Testing New Response Format")
    print("=" * 80)
    
    # Create a mock server instance
    qdrant_settings = QdrantSettings(
        qdrant_url=":memory:",
        collection_name="test"
    )
    embedding_settings = EmbeddingProviderSettings()
    tool_settings = ToolSettings()
    
    server = QdrantMCPServer(
        qdrant_settings=qdrant_settings,
        embedding_provider_settings=embedding_settings,
        tool_settings=tool_settings
    )
    
    # Create test entries
    test_entries = [
        Entry(
            content="Python is a high-level programming language known for its simplicity",
            metadata={
                "category": "programming",
                "language": "python",
                "filePath": "test_data.py",
                "startLine": 10,
                "endLine": 15
            }
        ),
        Entry(
            content="Machine learning is a subset of artificial intelligence",
            metadata={
                "category": "AI",
                "topic": "machine learning",
                "importance": "high"
            }
        ),
        Entry(
            content="The Eiffel Tower is a famous landmark in Paris, France",
            metadata={
                "category": "landmarks",
                "location": "Paris",
                "country": "France"
            }
        )
    ]
    
    print("\n✅ NEW FORMAT (Clean and Readable):\n")
    print("=" * 80)
    
    # Simulate the new format
    query = "test search"
    result_text = f"Found {len(test_entries)} result(s) for query: '{query}'\n"
    for idx, entry in enumerate(test_entries, 1):
        result_text += server.format_entry(entry, idx)
    
    print(result_text)
    
    print("\n" + "=" * 80)
    print("\n❌ OLD FORMAT (Hard to Read):\n")
    print("=" * 80)
    
    # Show what the old format looked like
    print(f"['Results for the query \\'{query}\\'',")
    for entry in test_entries:
        entry_metadata = json.dumps(entry.metadata) if entry.metadata else ""
        old_format = f"<entry><content>{entry.content}</content><metadata>{entry_metadata}</metadata></entry>"
        print(f" '{old_format}',")
    print("]")
    
    print("\n" + "=" * 80)
    print("\n📊 Comparison:\n")
    print("OLD FORMAT:")
    print("  ❌ XML-like tags")
    print("  ❌ Multiple array items")
    print("  ❌ Metadata as compact JSON string")
    print("  ❌ Hard to read and parse")
    print()
    print("NEW FORMAT:")
    print("  ✅ Clear separators (--- Result N ---)")
    print("  ✅ Single text response")
    print("  ✅ Pretty-printed metadata (indented)")
    print("  ✅ Easy to read and parse")
    print("  ✅ Shows result count upfront")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    test_format_entry()
    print("\n✅ The code fix has been applied!")
    print("\n🔄 To see this new format in Cursor:")
    print("   1. Restart Cursor to reload the MCP server")
    print("   2. OR: Disconnect and reconnect MCP servers in Cursor settings")
    print("   3. Test with: mcp_qdrant_qdrant-find(query='test')")
    print()

