#!/usr/bin/env python3
"""测试 FastMCP 工具注册"""
import sys
from fastmcp import FastMCP

print("Testing FastMCP...", file=sys.stderr, flush=True)

# Test 1: Simple FastMCP instance
mcp1 = FastMCP("test-server-1")

@mcp1.tool()
def simple_tool(text: str) -> str:
    """A simple test tool"""
    return f"You said: {text}"

print(f"\n[Test 1] Simple FastMCP", file=sys.stderr, flush=True)
print(f"  Server name: {mcp1.name}", file=sys.stderr, flush=True)
print(f"  Has _tools: {hasattr(mcp1, '_tools')}", file=sys.stderr, flush=True)
if hasattr(mcp1, '_tools'):
    print(f"  Tools: {list(mcp1._tools.keys())}", file=sys.stderr, flush=True)


# Test 2: FastMCP with manual tool registration
mcp2 = FastMCP("test-server-2")

def manual_tool(text: str) -> str:
    """Manually registered tool"""
    return f"Manual: {text}"

mcp2.tool(manual_tool, name="my-manual-tool", description="A manual tool")

print(f"\n[Test 2] Manual Registration", file=sys.stderr, flush=True)
print(f"  Server name: {mcp2.name}", file=sys.stderr, flush=True)
print(f"  Has _tools: {hasattr(mcp2, '_tools')}", file=sys.stderr, flush=True)
if hasattr(mcp2, '_tools'):
    print(f"  Tools: {list(mcp2._tools.keys())}", file=sys.stderr, flush=True)


# Test 3: Subclass like QdrantMCPServer
class TestMCPServer(FastMCP):
    def __init__(self):
        super().__init__(name="test-server-3")
        self.setup_tools()
    
    def setup_tools(self):
        def my_tool(text: str) -> str:
            """Tool in subclass"""
            return f"Subclass: {text}"
        
        self.tool(my_tool, name="subclass-tool", description="Subclass tool")

mcp3 = TestMCPServer()

print(f"\n[Test 3] Subclass with setup_tools()", file=sys.stderr, flush=True)
print(f"  Server name: {mcp3.name}", file=sys.stderr, flush=True)
print(f"  Has _tools: {hasattr(mcp3, '_tools')}", file=sys.stderr, flush=True)
if hasattr(mcp3, '_tools'):
    print(f"  Tools: {list(mcp3._tools.keys())}", file=sys.stderr, flush=True)

print("\n✓ All tests completed", file=sys.stderr, flush=True)

