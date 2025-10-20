"""
Custom server configuration with OpenAI-compatible embedding support.

Usage:
    # For OpenAI
    OPENAI_API_KEY="your-key" python -m mcp_server_qdrant.custom_server
    
    # For Ollama (local)
    OPENAI_BASE_URL="http://localhost:11434/v1" \\
    OPENAI_MODEL_NAME="nomic-embed-text" \\
    python -m mcp_server_qdrant.custom_server
    
    # For Azure OpenAI
    OPENAI_API_KEY="your-key" \\
    OPENAI_BASE_URL="https://your-resource.openai.azure.com/openai/deployments/your-deployment" \\
    python -m mcp_server_qdrant.custom_server
"""

import os
from mcp_server_qdrant.mcp_server import QdrantMCPServer
from mcp_server_qdrant.settings import (
    QdrantSettings,
    ToolSettings,
)
from mcp_server_qdrant.embeddings.openai_compatible import OpenAICompatibleProvider


def create_custom_server():
    """Create MCP server with OpenAI-compatible embedding provider."""
    
    # Get OpenAI configuration from environment
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model_name = os.getenv("OPENAI_MODEL_NAME", "text-embedding-ada-002")
    vector_size = int(os.getenv("OPENAI_VECTOR_SIZE", "1536"))
    
    # Create custom embedding provider
    embedding_provider = OpenAICompatibleProvider(
        model_name=model_name,
        api_key=api_key,
        base_url=base_url,
        vector_size=vector_size
    )
    
    # Create MCP server with custom provider
    mcp = QdrantMCPServer(
        tool_settings=ToolSettings(),
        qdrant_settings=QdrantSettings(),
        embedding_provider=embedding_provider,  # 直接注入自定义 provider
        name="mcp-server-qdrant-openai"
    )
    
    return mcp


# Create server instance
mcp = create_custom_server()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Server with OpenAI embeddings")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
    )
    args = parser.parse_args()
    
    mcp.run(transport=args.transport)
