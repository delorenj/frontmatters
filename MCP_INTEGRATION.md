# FastMCP Integration for Frontmatters

This document describes the FastMCP integration for the Frontmatters CLI tool.

## Architecture

The integration follows a **hybrid approach** that preserves the existing Typer/Agno CLI while adding MCP server capabilities:

```
frontmatters/
├── main.py           # Original CLI entry point (unchanged)
├── mcp_server.py     # New FastMCP server definition
├── hybrid.py         # Hybrid entry point (CLI or MCP)
└── commands/
    └── tree.py       # Original commands (unchanged)
```

## Installation

Install the updated dependencies:

```bash
pip install -e .
# or
uv pip install -e .
```

## Usage

### As Traditional CLI (unchanged)

```bash
# Original CLI still works exactly the same
frontmatters tree show --json
frontmatters tree show --depth 5
```

### As MCP Server

```bash
# Method 1: Using the dedicated MCP entry point
fastmcp run frontmatters.mcp_server:mcp

# Method 2: Using the hybrid entry point
python -m frontmatters.hybrid --mcp-server

# Method 3: Using environment variable
FRONTMATTERS_MODE=mcp python -m frontmatters.hybrid
```

### As MCP Client

Once the server is running, you can interact with it via MCP protocol:

```python
from fastmcp.client import FastMCPClient

client = FastMCPClient("http://localhost:8000")

# Call the tree_show_json tool
result = await client.call_tool(
    "tree_show_json",
    {
        "path": ".",
        "depth": 3,
        "show_description": True,
        "show_tags": False
    }
)
```

## Available MCP Tools

### `tree_show_json`
Returns the directory structure as JSON with frontmatter metadata.

**Parameters:**
- `path` (str): Directory path to display (default: ".")
- `depth` (int): Maximum depth to traverse (default: 3)
- `show_description` (bool): Include description from frontmatter (default: True)
- `show_tags` (bool): Include tags from frontmatter (default: False)

**Returns:** JSON string with directory tree structure

### `list_markdown_files`
Lists all markdown files in a directory.

**Parameters:**
- `path` (str): Directory to search (default: ".")
- `recursive` (bool): Search subdirectories (default: True)

**Returns:** List of markdown file paths

## Integration Benefits

1. **Zero disruption**: Existing CLI functionality unchanged
2. **Code reuse**: MCP tools directly use existing command logic
3. **Flexible deployment**: Can run as CLI, MCP server, or both
4. **Easy extension**: Add new MCP tools by wrapping existing commands

## Adding More MCP Tools

To expose more CLI commands as MCP tools, edit `mcp_server.py`:

```python
@mcp.tool()
async def your_new_tool(ctx: Context, param1: str) -> str:
    # Import and call existing command logic
    from frontmatters.commands.your_command import your_function
    return your_function(param1)
```

## Testing

Test the MCP integration:

```bash
# Start the server
fastmcp run frontmatters.mcp_server:mcp

# In another terminal, test with curl
curl -X POST http://localhost:8000/tools/tree_show_json \
  -H "Content-Type: application/json" \
  -d '{"path": ".", "depth": 2}'
```

## Next Steps

- Add more frontmatters commands as MCP tools
- Implement streaming for large directory trees
- Add authentication/authorization if needed
- Create Docker container for easy deployment