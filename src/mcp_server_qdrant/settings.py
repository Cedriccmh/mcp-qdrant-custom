from typing import Literal
import os
from pathlib import Path

from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from mcp_server_qdrant.embeddings.types import EmbeddingProviderType

# Load .env file from project root
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"[Settings] Loaded environment from {env_path}")
else:
    # Try to load from current working directory
    load_dotenv()
    print("[Settings] No .env file found in project root, using system environment variables")

DEFAULT_TOOL_STORE_DESCRIPTION = (
    "Keep the memory for later use, when you are asked to remember something."
)
DEFAULT_TOOL_FIND_DESCRIPTION = (
    "Look up memories in Qdrant. Use this tool when you need to: \n"
    " - Find memories by their content \n"
    " - Access memories for further analysis \n"
    " - Get some personal information about the user"
)

METADATA_PATH = "metadata"


class ToolSettings(BaseSettings):
    """
    Configuration for all the tools.
    """

    tool_store_description: str = Field(
        default=DEFAULT_TOOL_STORE_DESCRIPTION,
        validation_alias="TOOL_STORE_DESCRIPTION",
    )
    tool_find_description: str = Field(
        default=DEFAULT_TOOL_FIND_DESCRIPTION,
        validation_alias="TOOL_FIND_DESCRIPTION",
    )


class EmbeddingProviderSettings(BaseSettings):
    """
    Configuration for the embedding provider.
    """

    provider_type: EmbeddingProviderType = Field(
        default=EmbeddingProviderType.FASTEMBED,
        validation_alias="EMBEDDING_PROVIDER",
    )
    model_name: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        validation_alias="EMBEDDING_MODEL",
    )
    
    # OpenAI Compatible Settings
    openai_api_key: str | None = Field(
        default=None,
        validation_alias="OPENAI_API_KEY",
        description="API key for OpenAI or compatible services"
    )
    openai_base_url: str | None = Field(
        default=None,
        validation_alias="OPENAI_BASE_URL",
        description="Base URL for OpenAI API or compatible services (e.g., http://localhost:11434/v1 for Ollama)"
    )
    openai_vector_size: int | None = Field(
        default=None,
        validation_alias="OPENAI_VECTOR_SIZE",
        description="Vector size for the embedding model (e.g., 1536 for text-embedding-ada-002)"
    )
    openai_timeout: float = Field(
        default=30.0,
        validation_alias="OPENAI_TIMEOUT",
        description="Request timeout in seconds for OpenAI API calls"
    )


class FilterableField(BaseModel):
    name: str = Field(description="The name of the field payload field to filter on")
    description: str = Field(
        description="A description for the field used in the tool description"
    )
    field_type: Literal["keyword", "integer", "float", "boolean"] = Field(
        description="The type of the field"
    )
    condition: Literal["==", "!=", ">", ">=", "<", "<=", "any", "except"] | None = (
        Field(
            default=None,
            description=(
                "The condition to use for the filter. If not provided, the field will be indexed, but no "
                "filter argument will be exposed to MCP tool."
            ),
        )
    )
    required: bool = Field(
        default=False,
        description="Whether the field is required for the filter.",
    )


class QdrantSettings(BaseSettings):
    """
    Configuration for the Qdrant connector.
    """

    location: str | None = Field(default=None, validation_alias="QDRANT_URL")
    api_key: str | None = Field(default=None, validation_alias="QDRANT_API_KEY")
    collection_name: str | None = Field(
        default=None, validation_alias="COLLECTION_NAME"
    )
    local_path: str | None = Field(default=None, validation_alias="QDRANT_LOCAL_PATH")
    search_limit: int = Field(default=10, validation_alias="QDRANT_SEARCH_LIMIT")
    read_only: bool = Field(default=False, validation_alias="QDRANT_READ_ONLY")
    score_threshold: float | None = Field(
        default=None, 
        validation_alias="QDRANT_SCORE_THRESHOLD",
        description="Minimum similarity score threshold for search results (0.0-1.0 for cosine similarity). "
                    "Results with scores below this threshold will be filtered out. "
                    "Default is None (no filtering)."
    )

    filterable_fields: list[FilterableField] | None = Field(default=None)

    allow_arbitrary_filter: bool = Field(
        default=False, validation_alias="QDRANT_ALLOW_ARBITRARY_FILTER"
    )

    def filterable_fields_dict(self) -> dict[str, FilterableField]:
        if self.filterable_fields is None:
            return {}
        return {field.name: field for field in self.filterable_fields}

    def filterable_fields_dict_with_conditions(self) -> dict[str, FilterableField]:
        if self.filterable_fields is None:
            return {}
        return {
            field.name: field
            for field in self.filterable_fields
            if field.condition is not None
        }

    @model_validator(mode="after")
    def check_local_path_conflict(self) -> "QdrantSettings":
        if self.local_path:
            if self.location is not None or self.api_key is not None:
                raise ValueError(
                    "If 'local_path' is set, 'location' and 'api_key' must be None."
                )
        return self


class ServerSettings(BaseSettings):
    """
    Configuration for the MCP server.
    """
    
    port: int = Field(
        default=8765,
        validation_alias="PORT",
        description="Port for HTTP/SSE server"
    )
    fastmcp_port: int = Field(
        default=8765,
        validation_alias="FASTMCP_PORT",
        description="FastMCP server port"
    )
    qdrant_data_path: str | None = Field(
        default=None,
        validation_alias="QDRANT_DATA_PATH",
        description="Docker Qdrant data volume path"
    )


class LoggingSettings(BaseSettings):
    """
    Configuration for logging.
    """
    
    log_level: str = Field(
        default="INFO",
        validation_alias="LOG_LEVEL",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
