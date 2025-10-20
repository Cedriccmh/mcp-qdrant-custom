#!/usr/bin/env python3
"""检查 FastMCP 的内部结构"""
import sys
from fastmcp import FastMCP

mcp = FastMCP("test-server")

@mcp.tool()
def test_tool(text: str) -> str:
    """Test tool"""
    return text

print("FastMCP attributes:", file=sys.stderr, flush=True)
for attr in dir(mcp):
    if not attr.startswith('__'):
        print(f"  {attr}", file=sys.stderr, flush=True)

print("\n\nLooking for tool-related attributes:", file=sys.stderr, flush=True)
for attr in dir(mcp):
    if 'tool' in attr.lower() or 'function' in attr.lower():
        value = getattr(mcp, attr, None)
        if not callable(value):
            print(f"  {attr}: {type(value)} = {value}", file=sys.stderr, flush=True)

print("\n\nChecking mcp.mcp (internal FastMCP):", file=sys.stderr, flush=True)
if hasattr(mcp, 'mcp'):
    print(f"  Type: {type(mcp.mcp)}", file=sys.stderr, flush=True)
    for attr in dir(mcp.mcp):
        if 'tool' in attr.lower() and not attr.startswith('__'):
            value = getattr(mcp.mcp, attr, None)
            print(f"  mcp.{attr}: {type(value)}", file=sys.stderr, flush=True)

