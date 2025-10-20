# MCP Error -32602 Parameter Validation Fix

## Problem Diagnosed

**Error**: `MCP error -32602: Invalid request parameters`

### Root Cause

When `COLLECTION_NAME` is set in environment variables, the `make_partial_function` wrapper removes the `collection_name` parameter from the tool signature. However, the old implementation accepted ALL kwargs without validation, which could cause mismatches when:

1. MCP client (Cursor) has a cached schema with `collection_name` parameter
2. MCP server declares tool without `collection_name` (after `make_partial_function`)
3. Client tries to call with `collection_name` → MCP protocol rejects with error -32602

## Fix Applied

**File**: `src/mcp_server_qdrant/common/func_tools.py`

**Changes**:
- Added parameter validation in both async and sync wrappers
- Now explicitly rejects unexpected keyword arguments
- Provides clear error messages about what parameters are expected

### Before (Lines 16-25):
```python
async def async_wrapper(*args, **kwargs):
    bound_args = dict(fixed_values)
    for name, value in zip(remaining_params, args):
        bound_args[name] = value
    bound_args.update(kwargs)  # ❌ Accepts any kwargs
    return await original_func(**bound_args)
```

### After (Lines 16-33):
```python
async def async_wrapper(*args, **kwargs):
    bound_args = dict(fixed_values)
    
    # ✅ Validate that only expected parameters are passed
    unexpected_params = set(kwargs.keys()) - set(remaining_params)
    if unexpected_params:
        raise TypeError(
            f"Got unexpected keyword arguments: {', '.join(unexpected_params)}. "
            f"Expected parameters: {', '.join(remaining_params)}"
        )
    
    for name, value in zip(remaining_params, args):
        bound_args[name] = value
    bound_args.update(kwargs)
    return await original_func(**bound_args)
```

## Test Results

All tests pass:

```
[OK] Signature correctly modified
[OK] Valid call works correctly  
[OK] Correctly raised TypeError for unexpected parameters
```

The fix ensures:
1. ✅ Parameters are correctly removed from signature
2. ✅ Fixed values are used internally
3. ✅ Unexpected parameters are rejected with clear error messages

## How to Apply the Fix

### Step 1: Stop the MCP Server

If the server is currently running, stop it by pressing `Ctrl+C` in the terminal window.

### Step 2: Restart the MCP Server

Run the batch file to start the server with the updated code:

```batch
start_mcp_server.bat
```

The server will now use the fixed parameter validation logic.

### Step 3: Restart Cursor (If Needed)

If Cursor has cached the old tool schema:

1. Close and restart Cursor
2. Or reload the Cursor window: `Ctrl+Shift+P` → "Developer: Reload Window"

This will force Cursor to re-query the tool schemas from the MCP server.

### Step 4: Test the Tool

Try using the `mcp_qdrant_qdrant-find` tool:

```
Search for: "python programming"
```

**Important**: When `COLLECTION_NAME` is set in your environment (as it is in your `start_mcp_server.bat`), do NOT manually pass the `collection_name` parameter. The tool automatically uses the configured collection.

## Expected Behavior

### Correct Usage (with COLLECTION_NAME set):
```python
# ✅ Only pass query parameter
mcp_qdrant_qdrant-find(query="test")
```

### Incorrect Usage (will error):
```python
# ❌ Don't pass collection_name when it's set in environment
mcp_qdrant_qdrant-find(query="test", collection_name="ws-77b2ac62ce00ae8e")
# Error: Got unexpected keyword arguments: collection_name
```

## Environment Configuration

Your current configuration in `start_mcp_server.bat`:

```batch
set QDRANT_URL=http://localhost:6333
set COLLECTION_NAME=ws-77b2ac62ce00ae8e  ← This fixes collection_name
set EMBEDDING_PROVIDER=openai_compatible
set EMBEDDING_MODEL=Qwen/Qwen3-Embedding-8B
```

Because `COLLECTION_NAME` is set, the tool signature is:
- ✅ `qdrant-find(query: str)` 
- ❌ NOT `qdrant-find(query: str, collection_name: str)`

## Verification

To verify the fix is working, run:

```bash
uv run python test_signature_fix.py
```

You should see:
```
ALL TESTS PASSED [OK]
```

## Related Files

- `src/mcp_server_qdrant/common/func_tools.py` - Parameter validation fix
- `test_signature_fix.py` - Test to verify the fix
- `start_mcp_server.bat` - Server startup with environment configuration

## Summary

✅ **Fix applied and tested**  
✅ **Parameter validation now strict**  
✅ **Clear error messages for debugging**  

Next step: **Restart the MCP server and test the tool in Cursor**

