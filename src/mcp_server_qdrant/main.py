import argparse
import logging
import sys


def main():
    """
    Main entry point for the mcp-server-qdrant script defined
    in pyproject.toml. It runs the MCP server with a specific transport
    protocol.
    """
    
    # Get logging settings
    from mcp_server_qdrant.settings import LoggingSettings
    logging_settings = LoggingSettings()
    log_level = getattr(logging, logging_settings.log_level.upper(), logging.INFO)
    
    # Configure logging - MUST use stderr to not interfere with stdio transport
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stderr,
        force=True
    )
    logger = logging.getLogger(__name__)
    
    # Ensure stderr is unbuffered
    sys.stderr.reconfigure(line_buffering=True)
    
    # Filter the harmless FastMCP initialization race warning
    # This warning occurs when clients connect very quickly before
    # the MCP initialization handshake completes, but requests are
    # queued and processed correctly afterward
    class FastMCPInitWarningFilter(logging.Filter):
        def filter(self, record):
            if "Failed to validate request: Received request before initialization" in record.getMessage():
                return False  # Suppress this specific warning
            return True
    
    # Apply filter to root logger
    for handler in logging.getLogger().handlers:
        handler.addFilter(FastMCPInitWarningFilter())

    # Parse the command-line arguments to determine the transport protocol.
    parser = argparse.ArgumentParser(description="mcp-server-qdrant")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
    )
    args = parser.parse_args()
    
    logger.info(f"Starting MCP server with transport: {args.transport}")

    # Import is done here to make sure environment variables are loaded
    # only after we make the changes.
    try:
        from mcp_server_qdrant.server import mcp
        logger.info("Server module imported successfully")
        
        logger.info("Running MCP server...")
        mcp.run(transport=args.transport)
        logger.info("MCP server stopped")
    except Exception as e:
        logger.error(f"Failed to run MCP server: {e}", exc_info=True)
        raise
