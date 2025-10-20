#!/usr/bin/env python3
"""
Populate the running MCP server with test data
NOTE: This won't work because the server uses :memory: mode and is in a separate process!
"""
import requests
import json

# The running server endpoint
SERVER_URL = "http://localhost:8765"

print("=" * 80)
print("ATTEMPTING TO POPULATE DATABASE VIA HTTP")
print("=" * 80)
print("\nNOTE: This demonstrates the limitation of :memory: mode!")
print("The MCP server runs in a separate process with its own memory.")
print("Each Python script/process has its own in-memory database.\n")
print("=" * 80)
print("\nTO FIX THIS, you have two options:")
print("\n1. Use PERSISTENT storage instead of :memory:")
print("   Change in run_http_server.py:")
print('   os.environ["QDRANT_URL"] = ":memory:"')
print("   TO:")
print('   os.environ["QDRANT_LOCAL_PATH"] = "./qdrant_data"')
print('   # Remove QDRANT_URL line')
print("\n2. Store data through Cursor using the qdrant-store tool")
print("   Tell Cursor: 'Store this information using qdrant-store: ...'")
print("\n=" * 80)

