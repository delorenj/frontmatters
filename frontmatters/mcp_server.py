from fastmcp import FastMCP, Context
from pathlib import Path
import json
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontmatters.commands.tree import build_json_tree

# Initialize FastMCP server
mcp = FastMCP("frontmatters-mcp", dependencies=["python-frontmatter>=1.1.0"])


@mcp.tool()
async def tree_show_json(
    ctx: Context,
    path: str = ".",
    depth: int = 3,
    show_description: bool = True,
    show_tags: bool = False,
) -> str:
    """
    Display directory structure as JSON with frontmatter information.

    Args:
        path: Directory path to display as tree (default: current directory)
        depth: Maximum depth to traverse (default: 3)
        show_description: Include description field from frontmatter (default: True)
        show_tags: Include tags field from frontmatter (default: False)

    Returns:
        JSON representation of the directory tree with frontmatter metadata
    """
    directory = Path(path).resolve()

    if not directory.exists():
        raise ValueError(f"Path '{path}' does not exist")

    if not directory.is_dir():
        raise ValueError(f"Path '{path}' is not a directory")

    # Build the JSON tree using the existing function from tree.py
    tree_data = build_json_tree(
        directory,
        depth,
        show_description,
        show_tags
    )

    # Return as formatted JSON string
    return json.dumps(tree_data, indent=2, ensure_ascii=False)


# Optional: Add more MCP tools for other frontmatters commands
@mcp.tool()
async def list_markdown_files(
    ctx: Context,
    path: str = ".",
    recursive: bool = True,
) -> list[str]:
    """
    List all markdown files in a directory.

    Args:
        path: Directory path to search (default: current directory)
        recursive: Search subdirectories recursively (default: True)

    Returns:
        List of markdown file paths
    """
    directory = Path(path).resolve()

    if not directory.exists():
        raise ValueError(f"Path '{path}' does not exist")

    if not directory.is_dir():
        raise ValueError(f"Path '{path}' is not a directory")

    pattern = "**/*.md" if recursive else "*.md"
    markdown_files = [str(f) for f in directory.glob(pattern)]

    return sorted(markdown_files)