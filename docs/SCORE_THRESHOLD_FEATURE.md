# Score Threshold Feature Documentation

## Overview

The Score Threshold feature allows you to filter Qdrant search results based on their similarity scores. This helps ensure that only sufficiently relevant results are returned to the user.

## What is a Score Threshold?

When performing vector similarity searches in Qdrant, each result comes with a similarity score that indicates how closely the result matches your query. The score threshold acts as a minimum quality filter:

- **Results with scores >= threshold**: Included in the response
- **Results with scores < threshold**: Filtered out (not returned)

## Configuration

### Environment Variable

Add the following to your `.env` file:

```env
QDRANT_SCORE_THRESHOLD=0.5
```

### Configuration Details

- **Variable Name**: `QDRANT_SCORE_THRESHOLD`
- **Type**: Float (decimal number)
- **Range**: 0.0 to 1.0 (for cosine similarity)
- **Default**: None (no filtering applied)
- **Optional**: Yes

## Understanding Similarity Scores

The project uses **cosine similarity** by default, where:

- **Score = 1.0**: Perfect match (vectors point in exactly the same direction)
- **Score = 0.0**: Orthogonal (no similarity)
- **Score = -1.0**: Opposite direction (rarely seen in practice)

In practical use, most relevant results will have scores between 0.3 and 1.0.

## Recommended Threshold Values

| Threshold | Use Case | Description |
|-----------|----------|-------------|
| `0.3` | Exploratory search | Returns many results, including loosely related matches |
| `0.5` | Balanced search | Good balance between recall and precision |
| `0.7` | Precise search | Only returns highly relevant matches |
| `0.8+` | Very strict | Only near-exact matches |

### Choosing the Right Threshold

1. **Start with 0.5**: This is a good default for most use cases
2. **Too many irrelevant results?** Increase the threshold (e.g., 0.6 or 0.7)
3. **Too few results?** Decrease the threshold (e.g., 0.4 or 0.3)
4. **Monitor the scores**: Check the actual scores of returned results to understand the distribution

## How It Works

### Implementation Details

1. **Configuration Loading** (`settings.py`):
   - `QdrantSettings` now includes `score_threshold` field
   - Loaded from `QDRANT_SCORE_THRESHOLD` environment variable

2. **Connector Initialization** (`qdrant.py`):
   - `QdrantConnector` accepts `score_threshold` parameter
   - Stores it as `self._score_threshold`

3. **Search Execution** (`qdrant.py`):
   - The `search()` method now accepts optional `score_threshold` parameter
   - Uses provided threshold or falls back to connector's default
   - Passes threshold to Qdrant's `query_points()` API
   - Qdrant filters results server-side (efficient)

4. **MCP Server Integration** (`mcp_server.py`):
   - Passes threshold from settings to connector during initialization

### Code Flow

```
.env file
  ↓ (loaded by python-dotenv)
QdrantSettings.score_threshold
  ↓ (passed to)
QdrantConnector.__init__(score_threshold=...)
  ↓ (stored as)
self._score_threshold
  ↓ (used in)
QdrantConnector.search(...)
  ↓ (passed to)
qdrant_client.query_points(score_threshold=...)
```

## Examples

### Example 1: No Threshold (Default Behavior)

```env
# No QDRANT_SCORE_THRESHOLD set
```

**Result**: All results up to `QDRANT_SEARCH_LIMIT` are returned, regardless of score.

```
Results for query 'machine learning':
1. Score: 0.95 - "Introduction to Machine Learning"
2. Score: 0.87 - "Deep Learning Fundamentals"
3. Score: 0.72 - "Neural Networks Basics"
4. Score: 0.45 - "Data Science Overview"
5. Score: 0.23 - "Programming Basics"  ← May be irrelevant
```

### Example 2: Moderate Threshold

```env
QDRANT_SCORE_THRESHOLD=0.5
```

**Result**: Only results with score >= 0.5 are returned.

```
Results for query 'machine learning':
1. Score: 0.95 - "Introduction to Machine Learning"
2. Score: 0.87 - "Deep Learning Fundamentals"
3. Score: 0.72 - "Neural Networks Basics"
(Results with scores < 0.5 are filtered out)
```

### Example 3: Strict Threshold

```env
QDRANT_SCORE_THRESHOLD=0.8
```

**Result**: Only highly relevant results are returned.

```
Results for query 'machine learning':
1. Score: 0.95 - "Introduction to Machine Learning"
2. Score: 0.87 - "Deep Learning Fundamentals"
(Only 2 results met the threshold)
```

## Testing the Feature

### Quick Test Script

Create a test file `test_threshold.py`:

```python
import asyncio
import os
from mcp_server_qdrant.settings import QdrantSettings, EmbeddingProviderSettings
from mcp_server_qdrant.embeddings.factory import create_embedding_provider
from mcp_server_qdrant.qdrant import QdrantConnector

async def test_threshold():
    # Test with no threshold
    settings = QdrantSettings(
        location="http://localhost:6333",
        collection_name="test-collection",
        score_threshold=None
    )
    
    embedding_settings = EmbeddingProviderSettings()
    embedding_provider = create_embedding_provider(embedding_settings)
    
    connector = QdrantConnector(
        settings.location,
        settings.api_key,
        settings.collection_name,
        embedding_provider,
        score_threshold=settings.score_threshold
    )
    
    # Search without threshold
    results_no_threshold = await connector.search("test query", limit=10)
    print(f"Results without threshold: {len(results_no_threshold)}")
    for r in results_no_threshold:
        print(f"  Score: {r.score}")
    
    # Search with threshold
    results_with_threshold = await connector.search(
        "test query", 
        limit=10, 
        score_threshold=0.5
    )
    print(f"\nResults with threshold 0.5: {len(results_with_threshold)}")
    for r in results_with_threshold:
        print(f"  Score: {r.score}")

asyncio.run(test_threshold())
```

### Manual Testing Steps

1. **Set up your `.env` file** without threshold:
   ```env
   QDRANT_URL=http://localhost:6333
   COLLECTION_NAME=your-collection
   # QDRANT_SCORE_THRESHOLD not set
   ```

2. **Run the server and perform a search**:
   - Note the scores of returned results
   - Identify a score value in the middle range

3. **Add threshold to `.env`**:
   ```env
   QDRANT_SCORE_THRESHOLD=0.5  # Adjust based on observed scores
   ```

4. **Restart server and search again**:
   - Verify that low-scoring results are filtered out

## Troubleshooting

### Issue: No results returned after setting threshold

**Possible Causes:**
1. Threshold is set too high
2. Your query doesn't match well with the stored data
3. Embedding model mismatch

**Solutions:**
1. Lower the threshold (try 0.3 or 0.4)
2. Check that you're using the same embedding model for search as was used for storage
3. Try a different query

### Issue: Still seeing irrelevant results

**Possible Causes:**
1. Threshold is set too low
2. Data quality issues

**Solutions:**
1. Increase the threshold (try 0.6 or 0.7)
2. Review and improve the quality of stored data

## Best Practices

1. **Start Conservative**: Begin with no threshold or a low threshold (0.3-0.4)
2. **Monitor Scores**: Always display scores to users during development
3. **Adjust Based on Feedback**: Fine-tune based on actual result quality
4. **Document Your Choice**: Note why you chose a specific threshold
5. **Consider Use Case**: Different queries may benefit from different thresholds
6. **Test with Real Data**: Always test with your actual data, not just synthetic examples

## Performance Considerations

- **Server-Side Filtering**: The threshold is applied by Qdrant server-side, so it's very efficient
- **No Additional Overhead**: Filtering happens during the search, not after
- **Network Efficiency**: Fewer results mean less data transferred
- **Processing Efficiency**: Your application processes fewer results

## Migration Guide

If you have an existing deployment:

1. **No Breaking Changes**: The feature is optional and backward compatible
2. **Default Behavior Unchanged**: Without setting the variable, behavior is identical to before
3. **Gradual Rollout**: You can test on development first, then production
4. **Environment-Specific**: Use different thresholds for dev/staging/production

## API Reference

### QdrantSettings

```python
score_threshold: float | None = Field(
    default=None, 
    validation_alias="QDRANT_SCORE_THRESHOLD",
    description="Minimum similarity score threshold for search results"
)
```

### QdrantConnector.__init__()

```python
def __init__(
    self,
    ...,
    score_threshold: float | None = None,
):
    """
    :param score_threshold: Minimum score for search results
    """
```

### QdrantConnector.search()

```python
async def search(
    self,
    query: str,
    *,
    score_threshold: float | None = None,
) -> list[Entry]:
    """
    :param score_threshold: Override the connector's default threshold
    """
```

## Related Configuration

Works well with:

- `QDRANT_SEARCH_LIMIT`: Controls maximum number of results
- `QDRANT_READ_ONLY`: For read-only deployments
- Filterable fields: For combining score threshold with metadata filters

## Future Enhancements

Potential improvements:

1. Dynamic threshold adjustment based on query type
2. Per-collection threshold configuration
3. Threshold presets (low/medium/high)
4. Score normalization options
5. Percentile-based thresholds

## Conclusion

The Score Threshold feature provides fine-grained control over search result quality. By filtering out low-scoring results, you can improve the relevance of returned data and enhance user experience. Start with a moderate threshold (0.5) and adjust based on your specific needs and observed result quality.

