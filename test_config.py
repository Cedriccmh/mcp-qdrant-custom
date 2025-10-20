"""
测试配置是否正确
"""
import os
import sys

# 设置环境变量
os.environ["QDRANT_URL"] = ":memory:"
os.environ["COLLECTION_NAME"] = "test"
os.environ["EMBEDDING_PROVIDER"] = "openai_compatible"
os.environ["OPENAI_API_KEY"] = "sk-test"
os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn/v1"
os.environ["EMBEDDING_MODEL"] = "Qwen/Qwen3-Embedding-8B"
os.environ["OPENAI_VECTOR_SIZE"] = "4096"

try:
    print("=" * 60)
    print("开始测试配置...")
    print("=" * 60)
    
    # 1. 测试设置加载
    print("\n[1/4] 测试设置加载...")
    from mcp_server_qdrant.settings import (
        EmbeddingProviderSettings,
        QdrantSettings,
        ToolSettings,
    )
    
    embedding_settings = EmbeddingProviderSettings()
    qdrant_settings = QdrantSettings()
    tool_settings = ToolSettings()
    
    print(f"  ✓ Embedding Provider: {embedding_settings.provider_type}")
    print(f"  ✓ Model: {embedding_settings.model_name}")
    print(f"  ✓ Base URL: {embedding_settings.openai_base_url}")
    print(f"  ✓ Vector Size: {embedding_settings.openai_vector_size}")
    print(f"  ✓ Qdrant URL: {qdrant_settings.location}")
    print(f"  ✓ Collection: {qdrant_settings.collection_name}")
    
    # 2. 测试嵌入提供者创建
    print("\n[2/4] 测试嵌入提供者创建...")
    from mcp_server_qdrant.embeddings.factory import create_embedding_provider
    
    provider = create_embedding_provider(embedding_settings)
    print(f"  ✓ Provider类型: {type(provider).__name__}")
    print(f"  ✓ 向量维度: {provider.get_vector_size()}")
    print(f"  ✓ 向量名称: {provider.get_vector_name()}")
    
    # 3. 测试MCP服务器创建
    print("\n[3/4] 测试MCP服务器创建...")
    from mcp_server_qdrant.mcp_server import QdrantMCPServer
    
    mcp = QdrantMCPServer(
        tool_settings=tool_settings,
        qdrant_settings=qdrant_settings,
        embedding_provider_settings=embedding_settings,
    )
    print(f"  ✓ 服务器名称: {mcp.name}")
    print(f"  ✓ Qdrant连接器已创建")
    
    # 4. 显示工具列表
    print("\n[4/4] 可用的MCP工具:")
    if hasattr(mcp, '_tools'):
        for tool_name in mcp._tools:
            print(f"  ✓ {tool_name}")
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过！配置正确。")
    print("=" * 60)
    print("\n现在可以：")
    print("1. 重启 Cursor 让它加载新配置")
    print("2. 运行 debug_server.bat 使用 MCP Inspector 测试")
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

