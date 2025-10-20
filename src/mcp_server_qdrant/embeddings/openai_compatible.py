import asyncio
from typing import Optional
import httpx

from mcp_server_qdrant.embeddings.base import EmbeddingProvider


class OpenAICompatibleProvider(EmbeddingProvider):
    """
    OpenAI API compatible embedding provider.
    Supports OpenAI, Azure OpenAI, Ollama, and other compatible services.
    """
    
    def __init__(
        self,
        model_name: str = "text-embedding-ada-002",
        api_key: Optional[str] = None,
        base_url: str = "https://api.openai.com/v1",
        vector_size: int = 1536,
        timeout: float = 30.0
    ):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.vector_size = vector_size
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
        
    async def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """Embed a list of documents into vectors."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            
        payload = {
            "model": self.model_name,
            "input": documents
        }
        
        response = await self.client.post(
            f"{self.base_url}/embeddings",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        
        data = response.json()
        embeddings = [item["embedding"] for item in data["data"]]
        return embeddings
    
    async def embed_query(self, query: str) -> list[float]:
        """Embed a query into a vector."""
        embeddings = await self.embed_documents([query])
        return embeddings[0]
    
    def get_vector_name(self) -> str:
        """Get the name of the vector for the Qdrant collection."""
        # Use a consistent naming pattern
        model_short = self.model_name.replace("/", "-").replace(":", "-")
        return f"openai-{model_short}"
    
    def get_vector_size(self) -> int:
        """Get the size of the vector for the Qdrant collection."""
        return self.vector_size
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
