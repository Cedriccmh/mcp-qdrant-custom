import logging
import uuid
from typing import Any

from pydantic import BaseModel
from qdrant_client import AsyncQdrantClient, models

from mcp_server_qdrant.embeddings.base import EmbeddingProvider
from mcp_server_qdrant.settings import METADATA_PATH

logger = logging.getLogger(__name__)

Metadata = dict[str, Any]
ArbitraryFilter = dict[str, Any]


class Entry(BaseModel):
    """
    A single entry in the Qdrant collection.
    """

    content: str
    metadata: Metadata | None = None
    score: float | None = None


class QdrantConnector:
    """
    Encapsulates the connection to a Qdrant server and all the methods to interact with it.
    :param qdrant_url: The URL of the Qdrant server.
    :param qdrant_api_key: The API key to use for the Qdrant server.
    :param collection_name: The name of the default collection to use. If not provided, each tool will require
                            the collection name to be provided.
    :param embedding_provider: The embedding provider to use.
    :param qdrant_local_path: The path to the storage directory for the Qdrant client, if local mode is used.
    """

    def __init__(
        self,
        qdrant_url: str | None,
        qdrant_api_key: str | None,
        collection_name: str | None,
        embedding_provider: EmbeddingProvider,
        qdrant_local_path: str | None = None,
        field_indexes: dict[str, models.PayloadSchemaType] | None = None,
    ):
        self._qdrant_url = qdrant_url.rstrip("/") if qdrant_url else None
        self._qdrant_api_key = qdrant_api_key
        self._default_collection_name = collection_name
        self._embedding_provider = embedding_provider
        self._client = AsyncQdrantClient(
            location=qdrant_url, api_key=qdrant_api_key, path=qdrant_local_path
        )
        self._field_indexes = field_indexes
        self._collection_vector_config_cache: dict[str, Any] = {}

    async def get_collection_names(self) -> list[str]:
        """
        Get the names of all collections in the Qdrant server.
        :return: A list of collection names.
        """
        response = await self._client.get_collections()
        return [collection.name for collection in response.collections]

    async def _uses_unnamed_vectors(self, collection_name: str) -> bool:
        """
        Check if a collection uses unnamed vectors (simple list) or named vectors (dict).
        :param collection_name: The name of the collection to check.
        :return: True if collection uses unnamed vectors, False if it uses named vectors.
        """
        if collection_name in self._collection_vector_config_cache:
            return self._collection_vector_config_cache[collection_name]
        
        collection_exists = await self._client.collection_exists(collection_name)
        if not collection_exists:
            # New collection will be created - use named vectors by default
            self._collection_vector_config_cache[collection_name] = False
            return False
        
        # Get collection info to check vector configuration
        info = await self._client.get_collection(collection_name)
        vectors_config = info.config.params.vectors
        
        # If vectors is a VectorParams object directly (not dict), it's unnamed
        # If vectors is a dict, it has named vectors
        is_unnamed = not isinstance(vectors_config, dict)
        self._collection_vector_config_cache[collection_name] = is_unnamed
        
        logger.info(f"Collection '{collection_name}' uses {'unnamed' if is_unnamed else 'named'} vectors")
        return is_unnamed

    async def store(self, entry: Entry, *, collection_name: str | None = None):
        """
        Store some information in the Qdrant collection, along with the specified metadata.
        :param entry: The entry to store in the Qdrant collection.
        :param collection_name: The name of the collection to store the information in, optional. If not provided,
                                the default collection is used.
        """
        collection_name = collection_name or self._default_collection_name
        assert collection_name is not None
        await self._ensure_collection_exists(collection_name)

        # Embed the document
        # ToDo: instead of embedding text explicitly, use `models.Document`,
        # it should unlock usage of server-side inference.
        embeddings = await self._embedding_provider.embed_documents([entry.content])

        # Determine vector format based on collection configuration
        uses_unnamed = await self._uses_unnamed_vectors(collection_name)
        
        if uses_unnamed:
            # Use unnamed vector format (simple list)
            vector = embeddings[0]
        else:
            # Use named vector format (dictionary)
            vector_name = self._embedding_provider.get_vector_name()
            vector = {vector_name: embeddings[0]}
        
        # Add to Qdrant
        payload = {"document": entry.content, METADATA_PATH: entry.metadata}
        await self._client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=uuid.uuid4().hex,
                    vector=vector,
                    payload=payload,
                )
            ],
        )

    async def search(
        self,
        query: str,
        *,
        collection_name: str | None = None,
        limit: int = 10,
        query_filter: models.Filter | None = None,
    ) -> list[Entry]:
        """
        Find points in the Qdrant collection. If there are no entries found, an empty list is returned.
        :param query: The query to use for the search.
        :param collection_name: The name of the collection to search in, optional. If not provided,
                                the default collection is used.
        :param limit: The maximum number of entries to return.
        :param query_filter: The filter to apply to the query, if any.

        :return: A list of entries found.
        """
        collection_name = collection_name or self._default_collection_name
        collection_exists = await self._client.collection_exists(collection_name)
        if not collection_exists:
            return []

        # Embed the query
        # ToDo: instead of embedding text explicitly, use `models.Document`,
        # it should unlock usage of server-side inference.

        query_vector = await self._embedding_provider.embed_query(query)
        
        # Determine if we need to specify a vector name
        uses_unnamed = await self._uses_unnamed_vectors(collection_name)
        
        # Search in Qdrant
        if uses_unnamed:
            # For unnamed vectors, don't specify 'using' parameter
            search_results = await self._client.query_points(
                collection_name=collection_name,
                query=query_vector,
                limit=limit,
                query_filter=query_filter,
            )
        else:
            # For named vectors, specify which vector to use
            vector_name = self._embedding_provider.get_vector_name()
            search_results = await self._client.query_points(
                collection_name=collection_name,
                query=query_vector,
                using=vector_name,
                limit=limit,
                query_filter=query_filter,
            )

        # Parse results - handle both MCP format and other formats
        entries = []
        for result in search_results.points:
            # Extract score (available in query_points results)
            score = getattr(result, 'score', None)
            
            # Try MCP format first (document + metadata)
            if "document" in result.payload:
                entries.append(
                    Entry(
                        content=result.payload["document"],
                        metadata=result.payload.get(METADATA_PATH),
                        score=score,
                    )
                )
            # Handle code chunk format (codeChunk + other fields)
            elif "codeChunk" in result.payload:
                # Extract code chunk as content
                content = result.payload["codeChunk"]
                # Use other fields as metadata
                metadata = {k: v for k, v in result.payload.items() if k != "codeChunk"}
                entries.append(Entry(content=content, metadata=metadata, score=score))
            # Generic fallback: try to find any text-like field
            else:
                # Look for common text fields
                text_fields = ["text", "content", "body", "description"]
                content = None
                for field in text_fields:
                    if field in result.payload:
                        content = result.payload[field]
                        break
                
                if content is None:
                    # Use entire payload as string if no text field found
                    content = str(result.payload)
                    metadata = None
                else:
                    metadata = {k: v for k, v in result.payload.items() if k != field}
                
                entries.append(Entry(content=content, metadata=metadata, score=score))
        
        return entries

    async def _ensure_collection_exists(self, collection_name: str):
        """
        Ensure that the collection exists, creating it if necessary.
        :param collection_name: The name of the collection to ensure exists.
        """
        collection_exists = await self._client.collection_exists(collection_name)
        if not collection_exists:
            # Create the collection with the appropriate vector size
            vector_size = self._embedding_provider.get_vector_size()

            # Use the vector name as defined in the embedding provider
            vector_name = self._embedding_provider.get_vector_name()
            await self._client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    vector_name: models.VectorParams(
                        size=vector_size,
                        distance=models.Distance.COSINE,
                    )
                },
            )

            # Create payload indexes if configured

            if self._field_indexes:
                for field_name, field_type in self._field_indexes.items():
                    await self._client.create_payload_index(
                        collection_name=collection_name,
                        field_name=field_name,
                        field_schema=field_type,
                    )
