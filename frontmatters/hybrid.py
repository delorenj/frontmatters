#!/usr/bin/env python
"""
Hybrid entry point for Frontmatters - supports both CLI and MCP server modes.

Usage:
    # Run as CLI (default):
    python -m frontmatters.hybrid tree show

    # Run as MCP server:
    python -m frontmatters.hybrid --mcp-server

    # Or with environment variable:
    FRONTMATTERS_MODE=mcp python -m frontmatters.hybrid
"""

import os
import sys
import typer
from typing import Optional

# Import the existing CLI app
from frontmatters.main import app as cli_app

# Import the MCP server
from frontmatters.mcp_server import mcp


def run_mcp_server():
    """Run the FastMCP server."""
    import uvicorn
    from fastmcp.server import create_app

    # Create the FastAPI app from the MCP instance
    fastapi_app = create_app(mcp)

    # Run the server
    uvicorn.run(
        fastapi_app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )


def main():
    """
    Main entry point that decides whether to run as CLI or MCP server.
    """
    # Check if we should run as MCP server
    if "--mcp-server" in sys.argv:
        sys.argv.remove("--mcp-server")
        run_mcp_server()
    elif os.environ.get("FRONTMATTERS_MODE") == "mcp":
        run_mcp_server()
    else:
        # Run as regular CLI
        cli_app()


if __name__ == "__main__":
    main()