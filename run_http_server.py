#!/usr/bin/env python3
"""Run MCP server with HTTP/SSE transport to avoid Windows stdio issues"""
import os
import sys

# Load environment from .env file
from dotenv import load_dotenv
load_dotenv()

from mcp_server_qdrant.settings import ServerSettings

# Get server settings
server_settings = ServerSettings()
port = server_settings.port

print(f"Starting MCP server with SSE transport on port {port}...")
print(f"Configure Cursor to connect to: http://localhost:{port}/sse")
print("")
print("Configuration loaded from .env file")
print("")

from mcp_server_qdrant.server import mcp

# Run with SSE transport
try:
    mcp.run(transport="sse", port=port)
except KeyboardInterrupt:
    print("\nServer stopped.")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
