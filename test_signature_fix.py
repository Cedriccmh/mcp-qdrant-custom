#!/usr/bin/env python3
"""Test that the signature fix works correctly"""
import inspect
from typing import Annotated
from pydantic import Field
from src.mcp_server_qdrant.common.func_tools import make_partial_function


async def test_func(
    ctx,
    query: Annotated[str, Field(description="Query")],
    collection_name: Annotated[str, Field(description="Collection")] = "default",
):
    """Test function"""
    return f"Query: {query}, Collection: {collection_name}"


# Test 1: Check signature modification
print("=" * 60)
print("TEST 1: Signature Modification")
print("=" * 60)

original_sig = inspect.signature(test_func)
print(f"Original parameters: {list(original_sig.parameters.keys())}")

wrapped = make_partial_function(test_func, {"collection_name": "fixed-collection"})
wrapped_sig = inspect.signature(wrapped)
print(f"Wrapped parameters: {list(wrapped_sig.parameters.keys())}")

assert "collection_name" not in wrapped_sig.parameters, "collection_name should be removed"
assert "query" in wrapped_sig.parameters, "query should remain"
print("[OK] Signature correctly modified\n")

# Test 2: Check that calling with valid params works
print("=" * 60)
print("TEST 2: Valid Parameter Call")
print("=" * 60)

import asyncio


async def test_valid_call():
    class MockContext:
        pass

    result = await wrapped(MockContext(), query="test search")
    print(f"Result: {result}")
    assert "fixed-collection" in result
    print("[OK] Valid call works correctly\n")


asyncio.run(test_valid_call())

# Test 3: Check that calling with unexpected params raises error
print("=" * 60)
print("TEST 3: Invalid Parameter Call")
print("=" * 60)


async def test_invalid_call():
    class MockContext:
        pass

    try:
        result = await wrapped(
            MockContext(), query="test search", collection_name="should-fail"
        )
        print("[FAIL] Should have raised TypeError")
        return False
    except TypeError as e:
        print(f"[OK] Correctly raised TypeError: {e}\n")
        return True


success = asyncio.run(test_invalid_call())

if success:
    print("=" * 60)
    print("ALL TESTS PASSED [OK]")
    print("=" * 60)
    print("\nThe fix ensures that:")
    print("1. Parameters are correctly removed from signature")
    print("2. Fixed values are used internally")
    print("3. Unexpected parameters are rejected with clear error messages")
else:
    print("[FAIL] TEST FAILED")

