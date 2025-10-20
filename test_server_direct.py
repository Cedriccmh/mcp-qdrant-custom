#!/usr/bin/env python3
"""Test the MCP server directly via HTTP to diagnose the issue"""
import requests
import json

SERVER_URL = "http://localhost:8765"

print("=" * 80)
print("TESTING MCP SERVER DIRECTLY")
print("=" * 80)

# Test 1: Check if server is responding
print("\n1. Testing server connection...")
try:
    response = requests.get(f"{SERVER_URL}/health", timeout=5)
    print(f"   Server status: {response.status_code}")
except Exception as e:
    print(f"   [ERROR] Cannot connect to server: {e}")

# Test 2: List available tools
print("\n2. Listing available MCP tools...")
try:
    # MCP protocol: send initialization request
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }
    response = requests.post(f"{SERVER_URL}/mcp/v1", json=payload, timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   Tools available: {json.dumps(data, indent=2)}")
    else:
        print(f"   [ERROR] Status: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   [ERROR] {e}")

# Test 3: Call qdrant-find tool directly
print("\n3. Testing qdrant-find tool...")
try:
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "qdrant-find",
            "arguments": {
                "query": "test search"
            }
        }
    }
    response = requests.post(f"{SERVER_URL}/mcp/v1", json=payload, timeout=10)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Response: {json.dumps(data, indent=2)}")
    else:
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   [ERROR] {e}")

# Test 4: Check what's in the database using qdrant client
print("\n4. Checking database directly...")
try:
    import os
    os.environ["QDRANT_LOCAL_PATH"] = "./qdrant_data"
    
    from qdrant_client import QdrantClient
    
    client = QdrantClient(path="./qdrant_data")
    collections = client.get_collections()
    
    print(f"   Collections: {[c.name for c in collections.collections]}")
    
    for collection in collections.collections:
        info = client.get_collection(collection.name)
        print(f"\n   Collection '{collection.name}':")
        print(f"   - Vector count: {info.points_count}")
        print(f"   - Vector size: {info.config.params.vectors.size}")
        
except Exception as e:
    print(f"   [ERROR] {e}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)


