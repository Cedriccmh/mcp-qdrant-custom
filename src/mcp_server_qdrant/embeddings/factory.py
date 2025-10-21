from mcp_server_qdrant.embeddings.base import EmbeddingProvider
from mcp_server_qdrant.embeddings.types import EmbeddingProviderType
from mcp_server_qdrant.settings import EmbeddingProviderSettings


def create_embedding_provider(settings: EmbeddingProviderSettings) -> EmbeddingProvider:
    """
    Create an embedding provider based on the specified type.
    :param settings: The settings for the embedding provider.
    :return: An instance of the specified embedding provider.
    """
    if settings.provider_type == EmbeddingProviderType.FASTEMBED:
        from mcp_server_qdrant.embeddings.fastembed import FastEmbedProvider

        return FastEmbedProvider(settings.model_name)
    elif settings.provider_type == EmbeddingProviderType.OPENAI_COMPATIBLE:
        from mcp_server_qdrant.embeddings.openai_compatible import OpenAICompatibleProvider
        
        return OpenAICompatibleProvider(
            model_name=settings.model_name,
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url or "https://api.openai.com/v1",
            vector_size=settings.openai_vector_size or 1536,
            timeout=settings.openai_timeout
        )
    else:
        raise ValueError(f"Unsupported embedding provider: {settings.provider_type}")
