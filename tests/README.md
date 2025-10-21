# Test Suite Documentation

This folder contains automated tests for the Qdrant MCP server. Tests are organized by functionality and integration level.

---

## 📁 Directory Organization

### Tests Folder (`tests/`)

**Automated Tests:**
- `test_settings.py` - Configuration and environment variable tests
- `test_fastembed_integration.py` - FastEmbed provider tests
- `test_qdrant_integration.py` - Qdrant database integration tests
- `test_qdrant_find_tool.py` - End-to-end tool functionality tests
- `test_mcp_sse_client.py` - MCP protocol and SSE transport tests

**Utility Scripts:**
- `quick_test.py` - Quick server initialization smoke test
- `verify_fix.py` - Server functionality verification after changes
- `populate_default_collection.py` - Populate test data in Qdrant
- `test_score_threshold.py` - Test score threshold filtering feature
- `kill_port_8765.bat` - Kill process on port 8765 (Windows)

### Root Directory

**Server Operation:**
- `run_http_server.py` - Main server runner (SSE transport)
- `start_mcp_server.bat` - Windows startup script with auto port cleanup
- `debug_server.bat` - Debug mode with FastMCP inspector

**Security & Maintenance:**
- `check_security.ps1` - PowerShell security scanner
- `check_security.bat` - Batch security scanner

**Configuration:**
- `.env` - Environment variables (create from `.env.example`)
- `env.example` / `.env.example` - Environment variable templates

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

The `tests/` directory contains both automated tests and utility scripts for development and testing.

---

### Utility Scripts

#### `quick_test.py`
**Purpose**: Quick smoke test to verify server initialization.

**Location**: `tests/quick_test.py`

**Usage**:
```bash
uv run python tests/quick_test.py
```

**What it does**:
1. Loads configuration from `.env` file
2. Imports server module and verifies initialization
3. Checks embedding provider configuration
4. Validates Qdrant connection settings
5. Starts server in stdio mode for testing

**When to use**:
- Quick sanity check before running full test suite
- Verify configuration after making changes to `.env`
- Test server startup without full deployment
- Debug import or initialization errors

**Output**:
```
Quick Test - MCP Server Initialization
Configuration loaded from .env file

[1/3] Importing server module...
✓ Server module imported successfully

[2/3] Checking server configuration...
  - Embedding provider: OpenAICompatibleProvider
  - Vector size: 4096
  - Collection: your-collection-name
  - Qdrant URL: http://localhost:6333
✓ Configuration OK

[3/3] Testing stdio communication...
  Server is ready for stdio communication
```

---

#### `verify_fix.py`
**Purpose**: Verify server functionality after configuration changes.

**Location**: `tests/verify_fix.py`

**Usage**:
```bash
# Requires server running on http://localhost:8765
uv run python tests/verify_fix.py
```

**What it tests**:
1. SSE connection to running server
2. Tool invocation with realistic queries
3. Result validation and counting
4. Multiple query scenarios

**Test queries**:
- "embedding provider configuration"
- "qdrant search query"
- "MCP server initialization"

**When to use**:
- After restarting server to verify it works
- After changing search or embedding configuration
- To confirm server is returning results
- Quick integration test without full test suite

**Output**:
```
VERIFYING FIX - Testing Realistic Queries
1. Searching for 'embedding provider configuration'...
   Found 3 results
   Preview: Results for query 'embedding provider configuration':...

2. Searching for 'qdrant search query'...
   Found 5 results
   Preview: Results for query 'qdrant search query':...

✓ FIX VERIFIED - Server is returning results!
```

---

#### `populate_default_collection.py`
**Purpose**: Populate Qdrant collection with test data.

**Location**: `tests/populate_default_collection.py`

**Usage**:
```bash
uv run python tests/populate_default_collection.py
```

**What it does**:
1. Initializes Qdrant connector with settings from `.env`
2. Creates test entries about programming, AI, databases, protocols
3. Stores entries in the configured collection
4. Verifies storage by checking point count
5. Runs a test search to confirm functionality

**Test data includes**:
- Python programming language description
- JavaScript web development info
- Machine learning concepts
- Qdrant vector database information
- MCP protocol details

**When to use**:
- Initial setup of development environment
- After creating a new collection
- To reset test data to known state
- Before manual testing of search functionality
- Populate collection for demos

**Output**:
```
POPULATING DEFAULT COLLECTION WITH TEST DATA
1. Initializing Qdrant connector...
   Collection 'your-collection-name' exists: True
   Current points count: 0

2. Storing test data...
   1. Stored: Python is a high-level programming language...
   2. Stored: JavaScript is the language of the web...
   3. Stored: Machine learning is a subset of AI...
   4. Stored: Qdrant is a vector database...
   5. Stored: The MCP protocol enables seamless integration...

[OK] Stored 5 entries successfully

3. Verifying data storage...
   Total points in collection: 5

4. Testing semantic search...
   [OK] Found 3 results for 'programming languages'
```

**Prerequisites**:
- `.env` file configured with `COLLECTION_NAME`
- Qdrant server running (or `:memory:` mode configured)
- Valid embedding provider configured

---

#### `test_score_threshold.py`
**Purpose**: Test the score threshold filtering feature.

**Location**: `tests/test_score_threshold.py`

**Usage**:
```bash
uv run python tests/test_score_threshold.py
```

**What it tests**:
1. Configuration loading from `.env` file
2. Score threshold setting application
3. Search with default threshold (from settings)
4. Search with specific threshold override (0.5)
5. Search with strict threshold (0.8)
6. Result count comparison across different thresholds

**Test scenarios**:
- **Test 1**: Default threshold from `QDRANT_SCORE_THRESHOLD` environment variable
- **Test 2**: Override with moderate threshold (0.5)
- **Test 3**: Strict filtering with high threshold (0.8)

**When to use**:
- After implementing score threshold feature
- To verify threshold filtering works correctly
- After changing search or filtering logic
- To demonstrate threshold behavior with different values
- During configuration testing

**Output**:
```
SCORE THRESHOLD FEATURE TEST

Configuration:
  Qdrant URL: http://localhost:6333
  Collection: your-collection-name
  Search Limit: 20
  Score Threshold: 0.5
  Embedding Provider: openai_compatible
  Embedding Model: Qwen/Qwen3-Embedding-8B

TEST 1: Search with default threshold from settings
Query: 'artificial intelligence and neural networks'

Results: 4 entries found
  [1] Score: 0.8523
      Content: Deep learning uses neural networks with multiple layers
      Metadata: {'topic': 'DL'}
  ...

TEST 2: Search with threshold=0.5 (override)
Results: 3 entries found (filtered by score >= 0.5)
  ...

TEST 3: Search with threshold=0.8 (strict)
Results: 1 entries found (filtered by score >= 0.8)
  ...

TEST SUMMARY
Default threshold (from settings): 0.5
Results without filter: 4
Results with threshold=0.5: 3
Results with threshold=0.8: 1

[PASS] Test PASSED: Threshold filtering works as expected!
       (More strict thresholds return fewer or equal results)
```

**What it validates**:
- ✅ Score threshold is read from configuration
- ✅ Default threshold is applied to searches
- ✅ Per-search threshold overrides work
- ✅ Higher thresholds return fewer or equal results
- ✅ Filtering is working server-side in Qdrant

**Prerequisites**:
- `.env` file with `QDRANT_SCORE_THRESHOLD` configured
- Qdrant server running with test data
- Valid embedding provider configured
- Collection exists (script creates test data if needed)

---

#### `kill_port_8765.bat`
**Purpose**: Kill any process using port 8765 (default MCP server port).

**Location**: `tests/kill_port_8765.bat`

**Usage**:
```bash
tests\kill_port_8765.bat
```

**What it does**:
1. Checks for processes listening on port 8765
2. Identifies the PID using the port
3. Forcefully terminates the process
4. Verifies port is now free

**When to use**:
- Server didn't shut down cleanly
- Port conflict when starting server
- Before running integration tests
- During development when restarting frequently

**Output**:
```
========================================
Killing Process on Port 8765
========================================

Checking for processes using port 8765...
Found process(es) using port 8765:
  TCP    0.0.0.0:8765    LISTENING    12345

Attempting to kill...
Killing PID: 12345
SUCCESS: Port 8765 is now free!
```

**Note**: Windows-only script. Linux/Mac users can use:
```bash
lsof -ti:8765 | xargs kill -9
```

---

## Root Directory Scripts

These operational scripts remain in the root directory for easy access during development and deployment.

### Server Operation Scripts

#### `run_http_server.py`
**Purpose**: Main server runner with HTTP/SSE transport.

**Location**: Root directory

**Usage**:
```bash
uv run python run_http_server.py
```

**What it does**:
- Loads configuration from `.env` file
- Starts MCP server with SSE (Server-Sent Events) transport
- Runs on configured port (default: 8765)
- Provides endpoint at `http://localhost:8765/sse` for Cursor integration

**When to use**:
- Primary method for running the server
- Production deployment
- Integration with Cursor IDE
- When stdio transport has issues (Windows compatibility)

---

#### `start_mcp_server.bat`
**Purpose**: Windows batch script to start the server with automatic port cleanup.

**Location**: Root directory

**Usage**:
```bash
start_mcp_server.bat
```

**What it does**:
1. Loads configuration from `.env` file
2. Checks if port 8765 is in use
3. Automatically kills any process using the port
4. Starts `run_http_server.py`
5. Provides user-friendly console output

**When to use**:
- Quick server startup on Windows
- Development workflow with frequent restarts
- When you don't want to manually kill port processes
- Preferred method for Windows users

---

#### `debug_server.bat`
**Purpose**: Start server in debug mode with FastMCP inspector.

**Location**: Root directory

**Usage**:
```bash
debug_server.bat
```

**What it does**:
1. Sets environment variables (can override `.env`)
2. Enables FastMCP debug mode (`FASTMCP_DEBUG=true`)
3. Sets log level to DEBUG
4. Opens FastMCP Inspector in browser
5. Allows interactive testing of tools

**When to use**:
- Debugging tool implementations
- Testing tool parameters interactively
- Inspecting request/response payloads
- Development of new features
- Troubleshooting configuration issues

**Environment variables** (set in the script):
```batch
QDRANT_URL=http://localhost:6333
COLLECTION_NAME=your-collection-name
EMBEDDING_PROVIDER=openai_compatible
FASTMCP_DEBUG=true
FASTMCP_LOG_LEVEL=DEBUG
```

**Note**: Update the API key placeholder in the script or use `.env` file instead.

---

### Security and Maintenance Scripts

#### `check_security.ps1` / `check_security.bat`
**Purpose**: Pre-commit security checks to prevent leaking secrets.

**Location**: Root directory

**Usage**:
```bash
# PowerShell version
.\check_security.ps1

# Batch version
check_security.bat
```

**What it checks**:
1. **Hardcoded API keys**: Searches for `api_key="actual-value"` patterns
2. **OpenAI key patterns**: Finds `sk-` patterns (excludes placeholders)
3. **.env in .gitignore**: Verifies `.env` file is ignored
4. **.env staged for commit**: Prevents committing `.env` file
5. **Absolute paths** (PowerShell only): Finds hardcoded absolute paths

**When to use**:
- Before committing changes
- As a pre-commit git hook
- Before pushing to repository
- During code review
- After editing configuration files

**Output** (when issues found):
```
Security Check - Scanning for Hardcoded Secrets

[1/5] Checking for hardcoded API keys in scripts...
  ❌ FOUND: Potential hardcoded API keys:
     debug_server.bat:15:set OPENAI_API_KEY=sk-abc123...

[2/5] Checking for OpenAI key patterns...
  ✅ No OpenAI key patterns found

❌ SECURITY ISSUES FOUND!
Please fix the issues above before committing.
```

**Exit codes**:
- `0`: All checks passed, safe to commit
- `1`: Security issues found, do not commit

**Setting up as git hook**:
```bash
# Create pre-commit hook
echo ".\check_security.ps1" > .git/hooks/pre-commit
# or for batch
echo "call check_security.bat" > .git/hooks/pre-commit
```

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

