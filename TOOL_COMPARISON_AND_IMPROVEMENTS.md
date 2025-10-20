# Comparison: `mcp_qdrant_qdrant-find` vs `codebase_search`

**Date**: 2025-10-20  
**Analysis**: Complete Functional Testing & Comparison

---

## Executive Summary

Both tools perform **semantic search**, but they serve fundamentally different purposes:

- **`mcp_qdrant_qdrant-find`**: Memory/knowledge retrieval from a **persistent vector database**
- **`codebase_search`**: Live code exploration in the **current repository**

---

## Side-by-Side Comparison

| Feature | `mcp_qdrant_qdrant-find` | `codebase_search` |
|---------|-------------------------|-------------------|
| **Data Source** | Qdrant vector database | Live codebase files |
| **Search Scope** | Stored memories/data | Current repository code |
| **Persistence** | Data persists across sessions | Searches live files only |
| **Data Type** | Any text + metadata | Code files with line numbers |
| **Storage Required** | Must explicitly store data | No storage needed |
| **Result Format** | XML-like entries with metadata | Code chunks with citations |
| **Use Case** | Long-term memory, knowledge base | Code understanding, navigation |
| **Semantic Understanding** | ✅ Yes (embedding-based) | ✅ Yes (embedding-based) |
| **Configuration** | Requires Qdrant + embeddings | Built-in, ready to use |
| **Cross-session** | ✅ Yes | ❌ No |
| **Write Capability** | ✅ Can store new data | ❌ Read-only |

---

## Test Results

### Test Query 1: "How does semantic search work?"

**`mcp_qdrant_qdrant-find` returned:**
```xml
<entry>
  <content>print("1. Semantic search finds conceptually similar content, not just keyword matches")</content>
  <metadata>{"filePath": "test_semantic_search.py", "startLine": 148, ...}</metadata>
</entry>
```
- Returns 20 stored entries from database
- Mix of print statements and code from test files
- Includes duplicate entries (with/without segmentHash)
- Returns what was explicitly stored

**`codebase_search` returned:**
```python
# test_semantic_search.py (lines 1-156)
async def test_semantic_search():
    """
    Test semantic search with various queries to demonstrate
    that the search finds conceptually related content...
```
- Returns full function implementations
- Complete context with line numbers
- Clean, readable code blocks
- Live file content

---

### Test Query 2: "python programming"

**`mcp_qdrant_qdrant-find` returned:**
```xml
<entry>
  <content>print("TEST 1: Finding programming-related content")</content>
  <metadata>{"filePath": "test_qdrant_find_tool.py", ...}</metadata>
</entry>
<entry>
  <content>Entry(
    content="Python is a high-level programming language...",
    metadata={"category": "programming", "language": "python"}
  )</content>
</entry>
```
- Returns stored test data and print statements
- 20 results from database
- Mix of code snippets and test entries

**`codebase_search` returned:**
```python
# src/mcp_server_qdrant/main.py (lines 1-47)
def main():
    """
    Main entry point for the mcp-server-qdrant script...
```
- Returns actual Python source files
- Entry point functions and test files
- Complete implementations with context

---

### Test Query 3: "what is the collection name"

**`mcp_qdrant_qdrant-find` returned:**
```xml
<entry>
  <content>collection_name: Annotated[
    str, Field(description="The collection to search in")
  ]</content>
  <metadata>{"filePath": "src\\mcp_server_qdrant\\common\\wrap_filters.py", ...}</metadata>
</entry>
```
- Returns code snippets from database
- 20 entries referencing collection_name
- Includes annotations, print statements, function signatures

**`codebase_search` returned:**
```python
# src/mcp_server_qdrant/qdrant.py (lines 27-257)
class QdrantConnector:
    """
    Encapsulates the connection to a Qdrant server...
    :param collection_name: The name of the default collection to use...
    """
    def __init__(
        self,
        qdrant_url: str | None,
        qdrant_api_key: str | None,
        collection_name: str | None,
        ...
```
- Returns the main class implementation
- Shows how collection_name is used
- Complete context with docstrings

---

## Key Differences in Behavior

### 1. **Data Lifecycle**

**`mcp_qdrant_qdrant-find`:**
- Requires explicit storage: `await connector.store(entry)`
- Data persists in `./qdrant_data/` directory
- Survives server restarts
- Accumulates over time
- **Empty if no data has been stored**

**`codebase_search`:**
- Always searches current codebase
- No setup or storage needed
- Reflects current file state
- No persistence beyond files themselves

### 2. **Result Quality**

**`mcp_qdrant_qdrant-find`:**
- Quality depends on what was stored
- Can have noise (print statements, test data)
- May return duplicates (segmentHash variations)
- Returns exactly what was indexed

**`codebase_search`:**
- Automatically selects relevant code chunks
- Clean, syntactically complete results
- Provides file path + line numbers for navigation
- Better for understanding code structure

### 3. **Use Case Alignment**

**`mcp_qdrant_qdrant-find`:**
✅ Perfect for:
- Remembering user preferences
- Storing project notes/documentation
- Building a knowledge base
- Cross-project memory
- Semantic notes/bookmarks

❌ Not ideal for:
- Finding existing code in repo (use `codebase_search`)
- Understanding code structure (use `codebase_search`)
- One-time code searches

**`codebase_search`:**
✅ Perfect for:
- "Where is X implemented?"
- "How does Y work?"
- Understanding unfamiliar code
- Finding similar patterns
- Code navigation

❌ Not ideal for:
- Remembering conversation context
- Storing user notes
- Cross-session memory

---

## Current Issues with `mcp_qdrant_qdrant-find`

### 1. **Duplicate Results** ⚠️
```xml
<!-- Same content appears twice with/without segmentHash -->
<entry><content>...</content><metadata>{..., "segmentHash": "abc"}</metadata></entry>
<entry><content>...</content><metadata>{...}</metadata></entry>
```
**Impact**: Wastes space, confuses users  
**Severity**: Medium

### 2. **Noisy Results** ⚠️
```xml
<!-- Returns print statements instead of actual knowledge -->
<entry><content>print("TEST 5: Semantic Search for 'learning from data'")</content></entry>
```
**Impact**: Poor signal-to-noise ratio  
**Severity**: High (affects user experience)

### 3. **Fixed 20 Result Limit** ⚠️
- Always returns exactly 20 results (or fewer if not available)
- No way to request more or fewer
- Hardcoded in configuration

**Impact**: Users can't control result count  
**Severity**: Low to Medium

### 4. **Poor Result Formatting** ⚠️
Current format:
```xml
<entry><content>...</content><metadata>{...}</metadata></entry>
```
- Hard to read
- No scores shown
- No ranking indication
- Metadata not human-friendly

### 5. **No Result Ranking Indicators** ⚠️
- Results lack confidence scores
- No similarity percentage
- Can't tell best vs. worst match
- All results look equal

### 6. **Metadata Inconsistency** ⚠️
- Some entries have `segmentHash`, some don't
- Some have `pathSegments`, some don't
- Inconsistent metadata schemas
- Makes parsing difficult

---

## Recommendations for Improvement

### Priority 1: HIGH - Improve Result Quality

#### 1.1 **Add Result Deduplication**
```python
def format_entry(self, entry: Entry) -> str:
    """Format entry with deduplication."""
    # Current code creates duplicates - needs deduplication logic
    
    # Suggestion: Use content + file path as dedup key
    seen = set()
    unique_entries = []
    for entry in entries:
        key = (entry.content, entry.metadata.get("filePath"))
        if key not in seen:
            seen.add(key)
            unique_entries.append(entry)
    return unique_entries
```

**Benefit**: Eliminates duplicate results, cleaner output

#### 1.2 **Show Relevance Scores**
```python
def format_entry(self, entry: Entry) -> str:
    lines = []
    
    # Add score prominently
    if entry.score is not None:
        # Convert Qdrant cosine similarity to percentage
        similarity = (1 + entry.score) / 2 * 100  # Map [-1,1] to [0,100]
        lines.append(f"🎯 Relevance: {similarity:.1f}%")
    
    lines.append(f"📄 {entry.metadata.get('filePath', 'Unknown')}")
    lines.append(f"📝 {entry.content}")
    
    return "\n".join(lines)
```

**Benefit**: Users understand result quality, can trust top results

#### 1.3 **Improve Result Formatting**
Current (hard to read):
```xml
<entry><content>print("TEST 1...")</content><metadata>{"filePath": "test.py", ...}</metadata></entry>
```

Suggested (human-friendly):
```
🎯 Relevance: 87.3%
📄 File: test_semantic_search.py (lines 148-148)
📝 Content:
   print("1. Semantic search finds conceptually similar content, not just keyword matches")

---
```

**Benefit**: Much easier to scan and understand

### Priority 2: MEDIUM - Add Configurability

#### 2.1 **Make Limit Configurable**
```python
async def find(
    ctx: Context,
    query: Annotated[str, Field(description="What to search for")],
    collection_name: Annotated[str, Field(...)],
    limit: Annotated[int, Field(description="Max results to return", default=10)],
    query_filter: ArbitraryFilter | None = None,
) -> list[TextContent]:
    """Find with configurable limit."""
    entries = await self.qdrant_connector.search(
        query,
        collection_name=collection_name,
        limit=limit,  # User-specified, not hardcoded
        query_filter=query_filter,
    )
```

**Benefit**: Users can request 5 or 50 results as needed

#### 2.2 **Add Score Threshold Filtering**
```python
async def find(
    ...
    min_score: Annotated[float, Field(description="Minimum relevance (0-1)", default=0.0)],
) -> list[TextContent]:
    """Find with score filtering."""
    entries = await self.qdrant_connector.search(...)
    
    # Filter by score
    filtered_entries = [e for e in entries if e.score >= min_score]
    
    if not filtered_entries:
        return [TextContent(type="text", text=f"No results with score >= {min_score}")]
```

**Benefit**: Filter out low-quality matches automatically

### Priority 3: MEDIUM - Better Metadata Handling

#### 3.1 **Standardize Metadata Schema**
```python
class StandardMetadata(BaseModel):
    """Standard metadata for all entries."""
    filePath: str | None = None
    startLine: int | None = None
    endLine: int | None = None
    category: str | None = None
    timestamp: str | None = None
    # Remove segmentHash from results - internal only
```

**Benefit**: Consistent, predictable metadata structure

#### 3.2 **Add Metadata Validation on Store**
```python
async def store(
    ctx: Context,
    information: str,
    collection_name: str,
    metadata: Metadata | None = None,
) -> str:
    """Store with metadata validation."""
    # Validate and normalize metadata
    if metadata:
        validated_metadata = StandardMetadata(**metadata).model_dump(exclude_none=True)
    else:
        validated_metadata = None
    
    entry = Entry(content=information, metadata=validated_metadata)
```

**Benefit**: Cleaner, more reliable metadata

### Priority 4: LOW - Enhanced Features

#### 4.1 **Add Grouping by File**
```
Query: "semantic search"

📁 test_semantic_search.py (3 results)
  🎯 87.3% | Lines 148-148 | Semantic search finds conceptually similar content...
  🎯 82.1% | Lines 13-16  | Test semantic search with various queries...
  🎯 79.4% | Lines 150-150 | The search uses vector embeddings...

📁 test_qdrant_find_tool.py (2 results)
  🎯 76.5% | Lines 166-166 | The qdrant-find tool uses semantic search...
  🎯 71.2% | Lines 168-168 | Queries don't need exact keyword matches...
```

**Benefit**: Easier to scan, find relevant files

#### 4.2 **Add Result Statistics**
```
Query: "semantic search"
Found 15 results across 4 files
Top score: 87.3% | Average: 71.8%
---
```

**Benefit**: Quick overview of result quality

#### 4.3 **Support Result Filtering by Metadata**
```python
# Allow queries like:
results = await find(
    query="programming",
    collection_name="code",
    metadata_filter={"category": "python", "topic": "ai"}
)
```

**Benefit**: Powerful filtering capabilities

---

## Implementation Priority

### Phase 1: Quick Wins (1-2 hours)
1. ✅ Add relevance scores to output
2. ✅ Improve result formatting
3. ✅ Remove duplicate entries

### Phase 2: Core Improvements (3-5 hours)
1. ✅ Make result limit configurable
2. ✅ Add score threshold filtering
3. ✅ Standardize metadata schema

### Phase 3: Advanced Features (5-10 hours)
1. ⏳ Group results by file
2. ⏳ Add result statistics
3. ⏳ Enhanced metadata filtering

---

## Code Snippets: Ready to Implement

### Improved `format_entry` Method

```python
def format_entry(self, entry: Entry, show_score: bool = True) -> str:
    """
    Format a single entry in a human-readable way.
    
    Args:
        entry: The entry to format
        show_score: Whether to show relevance score
        
    Returns:
        Formatted string representation
    """
    lines = []
    
    # 1. Show relevance score prominently
    if show_score and entry.score is not None:
        # Convert Qdrant cosine similarity [-1, 1] to percentage [0%, 100%]
        similarity = (1 + entry.score) / 2 * 100
        lines.append(f"🎯 Relevance: {similarity:.1f}%")
    
    # 2. Show file location
    if entry.metadata:
        file_path = entry.metadata.get("filePath", "")
        start_line = entry.metadata.get("startLine", "")
        end_line = entry.metadata.get("endLine", "")
        
        if file_path:
            location = f"📄 File: {file_path}"
            if start_line and end_line:
                if start_line == end_line:
                    location += f" (line {start_line})"
                else:
                    location += f" (lines {start_line}-{end_line})"
            lines.append(location)
        
        # 3. Show other relevant metadata (exclude internal fields)
        metadata_to_show = {
            k: v for k, v in entry.metadata.items() 
            if k not in ["filePath", "startLine", "endLine", "segmentHash", "pathSegments"]
        }
        if metadata_to_show:
            lines.append(f"🏷️  Metadata: {metadata_to_show}")
    
    # 4. Show content
    lines.append(f"📝 Content:")
    # Indent content for readability
    content_lines = entry.content.split("\n")
    for line in content_lines:
        lines.append(f"   {line}")
    
    return "\n".join(lines)
```

### Improved `find` Method with Deduplication

```python
async def find(
    ctx: Context,
    query: Annotated[str, Field(description="What to search for")],
    collection_name: Annotated[
        str, Field(description="The collection to search in")
    ],
    limit: Annotated[
        int, 
        Field(description="Maximum number of results to return", default=10)
    ] = 10,
    min_score: Annotated[
        float,
        Field(description="Minimum relevance score (0.0-1.0)", default=0.0)
    ] = 0.0,
    query_filter: ArbitraryFilter | None = None,
) -> list[TextContent]:
    """
    Find memories in Qdrant with improved formatting and deduplication.
    """
    await ctx.debug(f"Finding results for query: {query}")
    await ctx.debug(f"Parameters: limit={limit}, min_score={min_score}")
    
    # Convert filter
    query_filter = models.Filter(**query_filter) if query_filter else None
    
    # Search with increased limit to account for deduplication
    raw_limit = min(limit * 2, 100)  # Get extra results for deduplication
    entries = await self.qdrant_connector.search(
        query,
        collection_name=collection_name,
        limit=raw_limit,
        query_filter=query_filter,
    )
    
    if not entries:
        return [TextContent(
            type="text", 
            text=f"No results found for the query '{query}'."
        )]
    
    # 1. Filter by minimum score
    if min_score > 0:
        entries = [e for e in entries if e.score and e.score >= min_score]
        if not entries:
            return [TextContent(
                type="text",
                text=f"No results found with relevance score >= {min_score:.2f}"
            )]
    
    # 2. Deduplicate entries
    seen = set()
    unique_entries = []
    for entry in entries:
        # Create dedup key from content + file location
        file_path = entry.metadata.get("filePath", "") if entry.metadata else ""
        dedup_key = (entry.content.strip(), file_path)
        
        if dedup_key not in seen:
            seen.add(dedup_key)
            unique_entries.append(entry)
            if len(unique_entries) >= limit:
                break
    
    # 3. Format results with header
    result_lines = [
        f"Results for the query '{query}':",
        f"Found {len(unique_entries)} unique result(s)",
        ""
    ]
    
    # Add statistics
    if unique_entries and unique_entries[0].score is not None:
        scores = [e.score for e in unique_entries if e.score is not None]
        if scores:
            avg_score = sum(scores) / len(scores)
            avg_pct = (1 + avg_score) / 2 * 100
            top_pct = (1 + scores[0]) / 2 * 100
            result_lines.append(f"📊 Top: {top_pct:.1f}% | Average: {avg_pct:.1f}%")
            result_lines.append("")
    
    # 4. Format each entry
    formatted_entries = []
    for i, entry in enumerate(unique_entries, 1):
        entry_text = self.format_entry(entry, show_score=True)
        formatted_entries.append(f"Result {i}:\n{entry_text}")
    
    result_lines.append("\n---\n\n".join(formatted_entries))
    result_text = "\n".join(result_lines)
    
    return [TextContent(type="text", text=result_text)]
```

---

## Conclusion

Both tools are **valuable but complementary**:

- **Use `codebase_search`** for: Understanding existing code, navigation, finding implementations
- **Use `mcp_qdrant_qdrant-find`** for: Long-term memory, notes, cross-session knowledge

### Key Recommendations:

1. **🔴 HIGH PRIORITY**: Fix duplicate results and improve formatting
2. **🟡 MEDIUM PRIORITY**: Add configurability (limit, score threshold)
3. **🟢 LOW PRIORITY**: Add advanced features (grouping, statistics)

The tool is **functional and useful**, but needs UX improvements to compete with `codebase_search` for code-related queries.

---

## Next Steps

1. Implement Phase 1 improvements (quick wins)
2. Test with real user queries
3. Gather feedback on new format
4. Proceed to Phase 2 if users are satisfied
5. Consider adding a "smart mode" that automatically chooses between file-based and database search

---

**Status**: Ready for implementation ✅

