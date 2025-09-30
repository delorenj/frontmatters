import os
import json
import re
import typer
from pathlib import Path
from frontmatters.core.processor import FrontmatterProcessor

app = typer.Typer()


def get_title_with_fallback(filepath: Path, processor: FrontmatterProcessor = None):
    """
    Get the title for a file with fallback logic:
    1. 'title' from frontmatter metadata
    2. First top-level heading from content
    3. Titleized version of the filename (without extension)
    """
    # For non-markdown files, just return titleized filename
    if filepath.suffix != ".md":
        return titleize_filename(filepath.name)

    try:
        # Use provided processor or create new one
        if processor is None:
            processor = FrontmatterProcessor(filepath)

        # 1. Check for 'title' in frontmatter
        if processor.has_frontmatter("title"):
            return processor.post.metadata["title"]

        # 2. Look for first top-level heading
        content = processor.content
        heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if heading_match:
            return heading_match.group(1).strip()

        # 3. Fall back to titleized filename
        return titleize_filename(filepath.stem)

    except Exception:
        # If any error occurs, use titleized filename
        return titleize_filename(filepath.stem if filepath.suffix == ".md" else filepath.name)


def titleize_filename(filename: str):
    """Convert a filename to a title format."""
    # Remove file extension if present
    name = filename

    # Replace underscores and hyphens with spaces
    name = name.replace('_', ' ').replace('-', ' ')

    # Capitalize each word
    words = name.split()
    titleized = ' '.join(word.capitalize() for word in words)

    return titleized


def format_tree_line(path: Path, level: int, is_last: bool, parent_is_last: list, frontmatter_data: str = ""):
    """Format a single line of the tree output with proper indentation and connectors."""
    prefix = ""
    
    # Build the prefix based on the tree structure
    for i in range(level):
        if i < len(parent_is_last):
            if parent_is_last[i]:
                prefix += "    "  # Empty space for completed branches
            else:
                prefix += "│   "  # Vertical line for ongoing branches
        else:
            prefix += "    "
    
    # Add the connector for this item
    if is_last:
        prefix += "└── "
    else:
        prefix += "├── "
    
    # Format the line with filename and frontmatter data
    line = f"{prefix}{path.name}"
    if frontmatter_data:
        line += f" {frontmatter_data}"
    
    return line


def get_frontmatter_display(filepath: Path, show_description: bool, show_tags: bool):
    """Extract and format frontmatter data for display."""
    if not filepath.suffix == ".md":
        return ""
    
    try:
        processor = FrontmatterProcessor(filepath)
        parts = []
        
        if show_description and processor.has_frontmatter("description"):
            desc = processor.post.metadata["description"]
            # Truncate long descriptions
            if len(desc) > 60:
                desc = desc[:57] + "..."
            parts.append(f"[{desc}]")
        
        if show_tags and processor.has_frontmatter("tags"):
            tags = processor.post.metadata["tags"]
            if isinstance(tags, list):
                tag_str = ", ".join(tags)
            else:
                tag_str = str(tags)
            # Truncate long tag lists
            if len(tag_str) > 40:
                tag_str = tag_str[:37] + "..."
            parts.append(f"#{tag_str}")
        
        if parts:
            return f" {' '.join(parts)}"
        
    except Exception:
        # Silently ignore files that can't be processed
        pass
    
    return ""


def build_json_tree(directory: Path, max_depth: int, show_description: bool, show_tags: bool, current_depth: int = 0):
    """Build a JSON representation of the directory tree with frontmatter."""
    if current_depth >= max_depth:
        return None

    try:
        result = {
            "title": titleize_filename(directory.name),
            "path": str(directory),
            "type": "directory",
            "children": []
        }

        entries = list(directory.iterdir())

        # Sort: directories first, then files, both alphabetically
        directories = sorted([p for p in entries if p.is_dir() and not p.name.startswith('.')],
                           key=lambda x: x.name.lower())
        files = sorted([p for p in entries if p.is_file() and not p.name.startswith('.')],
                      key=lambda x: x.name.lower())

        # Add directories
        for dir_path in directories:
            child = build_json_tree(dir_path, max_depth, show_description, show_tags, current_depth + 1)
            if child:
                result["children"].append(child)

        # Add files
        for file_path in files:
            # Get the title with fallback logic
            processor = None
            if file_path.suffix == ".md":
                try:
                    processor = FrontmatterProcessor(file_path)
                except Exception:
                    pass

            file_data = {
                "title": get_title_with_fallback(file_path, processor),
                "path": str(file_path),
                "type": "file"
            }

            # Add frontmatter data if it's a markdown file
            if file_path.suffix == ".md" and processor:
                try:
                    frontmatter_data = {}

                    if show_description and processor.has_frontmatter("description"):
                        frontmatter_data["description"] = processor.post.metadata["description"]

                    if show_tags and processor.has_frontmatter("tags"):
                        frontmatter_data["tags"] = processor.post.metadata["tags"]

                    if frontmatter_data:
                        file_data["frontmatter"] = frontmatter_data

                except Exception:
                    # Silently ignore files that can't be processed
                    pass

            result["children"].append(file_data)

        return result

    except PermissionError:
        return None


def collect_tree_items(directory: Path, max_depth: int, current_depth: int = 0):
    """Recursively collect all items for the tree, sorted appropriately."""
    if current_depth >= max_depth:
        return []

    try:
        items = []
        entries = list(directory.iterdir())

        # Sort: directories first, then files, both alphabetically
        directories = sorted([p for p in entries if p.is_dir() and not p.name.startswith('.')],
                           key=lambda x: x.name.lower())
        files = sorted([p for p in entries if p.is_file() and not p.name.startswith('.')],
                      key=lambda x: x.name.lower())

        all_items = directories + files

        # Add directories
        for i, dir_path in enumerate(directories):
            is_last = (i == len(all_items) - 1)  # Last among all items
            items.append((dir_path, current_depth, is_last, True))

            # Recursively add subdirectory contents
            sub_items = collect_tree_items(dir_path, max_depth, current_depth + 1)
            items.extend(sub_items)

        # Add files
        for i, file_path in enumerate(files):
            file_index = len(directories) + i
            is_last = (file_index == len(all_items) - 1)
            items.append((file_path, current_depth, is_last, False))

        return items

    except PermissionError:
        return []


@app.command()
def show(
    path: Path = typer.Argument(Path("."), help="Directory to display as tree"),
    depth: int = typer.Option(3, "--depth", "-d", help="Maximum depth to traverse"),
    description: bool = typer.Option(True, "--description/--no-description", help="Show description field from frontmatter"),
    tags: bool = typer.Option(False, "--tags", "-t", help="Show tags field from frontmatter"),
    both: bool = typer.Option(False, "--both", "-b", help="Show both description and tags"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON instead of tree format"),
    output_file: Path = typer.Option(None, "--output", "-o", help="Write output to file instead of stdout"),
):
    """
    Display directory structure as a tree with frontmatter information.

    By default, shows only the description field for markdown files.
    Use --tags to show only tags, or --both to show both description and tags.
    Use --json to output structured JSON data instead of tree format.
    Use --output to write results to a file.
    """
    if not path.exists():
        typer.echo(f"Error: Path '{path}' does not exist", err=True)
        raise typer.Exit(1)
    
    if not path.is_dir():
        typer.echo(f"Error: Path '{path}' is not a directory", err=True)
        raise typer.Exit(1)
    
    # Handle flag combinations
    show_description = description and not tags  # Default behavior unless --tags is specified
    show_tags = tags or both
    if both:
        show_description = True

    # Generate output
    if json_output:
        # Build JSON tree
        tree_data = build_json_tree(path, depth, show_description, show_tags)
        output = json.dumps(tree_data, indent=2, ensure_ascii=False)
    else:
        # Build text tree
        lines = [f"{path.name}/"]

        # Collect and display all items
        items = collect_tree_items(path, depth)

        # Track which parent levels are the last in their respective directories
        parent_is_last = []

        for i, (item_path, level, is_last, is_directory) in enumerate(items):
            # Update parent_is_last list for current level
            if level >= len(parent_is_last):
                parent_is_last.extend([False] * (level + 1 - len(parent_is_last)))

            # Set current level's last status
            parent_is_last[level] = is_last

            # Get frontmatter data if it's a markdown file
            frontmatter_data = ""
            if not is_directory:
                frontmatter_data = get_frontmatter_display(item_path, show_description, show_tags)

            # Format the line
            line = format_tree_line(item_path, level, is_last, parent_is_last[:level], frontmatter_data)
            lines.append(line)

        output = "\n".join(lines)

    # Write output
    if output_file:
        output_file.write_text(output, encoding='utf-8')
        typer.echo(f"Output written to {output_file}")
    else:
        typer.echo(output)


if __name__ == "__main__":
    app()
