# Test Suite Documentation

This folder contains automated tests for the Qdrant MCP server. Tests are organized by functionality and integration level.

---

## Running Tests

### Run All Tests
```bash
# Using pytest
uv run pytest tests/

# Run with verbose output
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=mcp_server_qdrant
```

### Run Specific Test Files
```bash
# Unit tests
uv run pytest tests/test_settings.py
uv run pytest tests/test_fastembed_integration.py
uv run pytest tests/test_qdrant_integration.py

# Integration tests
uv run python tests/test_qdrant_find_tool.py
uv run python tests/test_mcp_sse_client.py
```

---

## Test Files

### Unit Tests

#### `test_settings.py`
**Purpose**: Test configuration settings and environment variable handling.

**What it tests**:
- `QdrantSettings` class initialization
- `EmbeddingProviderSettings` configuration
- `ToolSettings` parameters
- Environment variable validation
- Default values and overrides

**Example**:
```python
def test_qdrant_settings_from_env():
    os.environ["COLLECTION_NAME"] = "test-collection"
    settings = QdrantSettings()
    assert settings.collection_name == "test-collection"
```

**When to run**: After changing `settings.py` or configuration logic.

---

#### `test_fastembed_integration.py`
**Purpose**: Test FastEmbed embedding provider integration.

**What it tests**:
- FastEmbed model initialization
- Document embedding generation
- Query embedding generation
- Vector size validation
- Model loading and caching

**Dependencies**: Requires FastEmbed library and model downloads.

**Example**:
```python
async def test_fastembed_embed():
    provider = FastEmbedProvider(model="sentence-transformers/all-MiniLM-L6-v2")
    embeddings = await provider.embed_documents(["test text"])
    assert len(embeddings[0]) == 384
```

**When to run**: After changes to `embeddings/fastembed.py`.

---

#### `test_qdrant_integration.py`
**Purpose**: Test Qdrant client integration and database operations.

**What it tests**:
- Qdrant client initialization
- Collection creation and management
- Point insertion (upsert)
- Vector search queries
- Named vs unnamed vector handling
- Multiple collection support

**Dependencies**: Requires Qdrant running on `localhost:6333` or uses `:memory:` mode.

**Key scenarios**:
```python
# Test unnamed vectors
async def test_unnamed_vectors():
    connector = QdrantConnector(url, None, "test-collection", provider)
    await connector.store(Entry(content="test", metadata={}))
    results = await connector.search("test")
    assert len(results) > 0

# Test named vectors  
async def test_named_vectors():
    # Collection with named vectors
    results = await connector.search("query", collection_name="named-collection")
```

**When to run**: After changes to `qdrant.py` or search logic.

---

### Integration Tests

#### `test_qdrant_find_tool.py`
**Purpose**: End-to-end test of the `qdrant-find` tool functionality.

**What it tests**:
- Full workflow: initialize → store → find
- Semantic search with real embeddings
- Multiple query types (programming, AI, landmarks)
- Result ranking and relevance
- Metadata storage and retrieval
- In-memory Qdrant mode

**Test data**:
```python
test_data = [
    {"information": "Python is a versatile programming language...", 
     "metadata": {"category": "programming"}},
    {"information": "Machine learning involves...",
     "metadata": {"category": "AI"}},
    # ... more test entries
]
```

**Test queries**:
1. "programming languages for web development" → Should find Python, JavaScript
2. "artificial intelligence and neural computation" → Should find ML, neural networks
3. "famous tourist attractions" → Should find landmarks
4. "quantum physics" → Tests low-similarity results

**Output example**:
```
TEST 1: Finding programming-related content
Query: 'programming languages for web development'
Found 3 results:
1. Python is a versatile programming language...
   Metadata: {'category': 'programming', 'language': 'python'}
```

**When to run**: 
- After changes to search functionality
- Before major releases
- To verify end-to-end workflow

**Runtime**: ~5-10 seconds (includes model loading)

---

#### `test_mcp_sse_client.py`
**Purpose**: Test MCP server via SSE (Server-Sent Events) transport.

**What it tests**:
- SSE connection to running server
- MCP protocol handshake and initialization
- Tool listing via MCP protocol
- Tool invocation (`qdrant-find`, `qdrant-store`)
- Response format validation
- Connection error handling

**Prerequisites**:
- MCP server must be running on `http://localhost:8765/sse`
- Start server: `uv run python run_http_server.py`

**Test flow**:
```
1. Connect to SSE endpoint
2. Initialize MCP session
3. List available tools
4. Call qdrant-find tool with test query
5. Validate response format
6. Call with different queries
```

**Output example**:
```
TESTING MCP SERVER VIA SSE
✓ Connected successfully!
✓ Session initialized!

Found 2 tools:
- qdrant-find: Look up memories in Qdrant...
- qdrant-store: Keep the memory for later use...

Testing qdrant-find tool with query 'test'...
Response: Results for the query 'test':
File path: test.py
Score: 0.85
Lines: 10-15
Code Chunk: def test_function():...
```

**When to run**:
- After changes to `mcp_server.py`
- After protocol changes
- To verify SSE transport works
- Before deploying server

**Common issues**:
- `Connection refused`: Server not running → Start server first
- `No results found`: Collection not configured → Check `COLLECTION_NAME` env var
- `Invalid parameters`: Schema mismatch → Restart server

**Runtime**: ~2-3 seconds (excluding server startup)

---

## Test Utilities

### Development/Utility Scripts (Root Directory)

These scripts are kept in the root directory for development convenience:

#### `quick_test.py`
**Purpose**: Quick smoke test to verify server can start.

```bash
uv run python quick_test.py
```

**Use case**: Verify configuration before running full test suite.

---

#### `verify_fix.py`
**Purpose**: Verify server is working after configuration changes.

```bash
uv run python verify_fix.py
```

**Use case**: After restarting server, verify it can find results.

---

#### `populate_default_collection.py`
**Purpose**: Populate Qdrant with sample code chunks from the project.

```bash
uv run python populate_default_collection.py
```

**Use case**: Set up test data for development and testing.

---

## Test Data Management

### In-Memory Testing
For unit and integration tests, use `:memory:` mode:

```python
os.environ["QDRANT_URL"] = ":memory:"
```

**Advantages**:
- Fast (no network calls)
- Isolated (no side effects)
- No cleanup needed

### Persistent Testing
For SSE client tests, use actual Qdrant instance:

```python
os.environ["QDRANT_URL"] = "http://localhost:6333"
os.environ["COLLECTION_NAME"] = "test-collection"
```

**Use case**: Testing against real database with actual data.

---

## Writing New Tests

### Unit Test Template
```python
import pytest
from mcp_server_qdrant.module import YourClass

@pytest.mark.asyncio
async def test_your_feature():
    """Test description"""
    # Setup
    instance = YourClass(param="value")
    
    # Execute
    result = await instance.method()
    
    # Assert
    assert result == expected_value
```

### Integration Test Template
```python
import asyncio
import os

os.environ["QDRANT_URL"] = ":memory:"
os.environ["COLLECTION_NAME"] = "test"

async def test_integration():
    """Test description"""
    from mcp_server_qdrant.mcp_server import QdrantMCPServer
    from mcp_server_qdrant.settings import QdrantSettings, EmbeddingProviderSettings, ToolSettings
    
    server = QdrantMCPServer(
        tool_settings=ToolSettings(),
        qdrant_settings=QdrantSettings(),
        embedding_provider_settings=EmbeddingProviderSettings(),
    )
    
    # Test operations
    results = await server.qdrant_connector.search("test query")
    assert len(results) > 0

if __name__ == "__main__":
    asyncio.run(test_integration())
```

---

## Debugging Failed Tests

### Common Issues

**1. Import Errors**
```
ModuleNotFoundError: No module named 'mcp_server_qdrant'
```
**Solution**: Run from project root using `uv run`.

**2. Environment Variables Not Set**
```
collection_name: None
```
**Solution**: Set env vars before importing:
```python
import os
os.environ["COLLECTION_NAME"] = "test-collection"
# THEN import modules
from mcp_server_qdrant.settings import QdrantSettings
```

**3. Qdrant Connection Fails**
```
Connection refused on localhost:6333
```
**Solution**: 
- Use `:memory:` mode for unit tests
- Start Qdrant for integration tests: `docker run -p 6333:6333 qdrant/qdrant`

**4. Embedding Model Download**
```
Downloading model...
```
**Solution**: First run takes longer. Models are cached afterwards.

---

## Test Coverage

To generate coverage report:

```bash
uv run pytest tests/ --cov=mcp_server_qdrant --cov-report=html
open htmlcov/index.html
```

**Target coverage**: >80% for core modules:
- `qdrant.py` (search logic)
- `mcp_server.py` (tool handlers)
- `settings.py` (configuration)
- `embeddings/` (embedding providers)

---

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: astral-sh/setup-uv@v1
      - run: uv run pytest tests/
```

---

## Performance Benchmarks

| Test File | Runtime | Notes |
|-----------|---------|-------|
| `test_settings.py` | <1s | Fast, no I/O |
| `test_fastembed_integration.py` | ~5s | Model loading |
| `test_qdrant_integration.py` | ~2s | In-memory mode |
| `test_qdrant_find_tool.py` | ~10s | Full workflow |
| `test_mcp_sse_client.py` | ~3s | Requires running server |

**Total suite runtime**: ~20 seconds

---

## Maintenance

### When to Update Tests

- **After code changes**: Update corresponding test file
- **New features**: Add new test cases
- **Bug fixes**: Add regression test
- **API changes**: Update integration tests
- **Deprecations**: Remove obsolete tests

### Test Cleanup Checklist

- [ ] Remove one-off debugging scripts
- [ ] Keep only reusable tests
- [ ] Update test documentation
- [ ] Verify all tests pass
- [ ] Check test coverage

---

## Related Documentation

- **Main README**: `../README.md` - Project overview
- **Configuration**: `../docs/CONFIG.md` - Setup guide
- **Debugging**: `../docs/DEBUGGING_GUIDE.md` - Troubleshooting
- **API Docs**: `../docs/` - API reference

---

## Questions?

For test-related questions or issues:
1. Check this README
2. Review `../docs/DEBUGGING_GUIDE.md`
3. Look at existing test examples
4. Check test output for error messages

