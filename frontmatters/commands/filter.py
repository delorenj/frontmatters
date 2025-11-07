"""Filter markdown files by frontmatter criteria."""

import json
import os
from pathlib import Path
from typing import List, Optional, Any

import typer
from rich.console import Console
from rich.table import Table

from frontmatters.core.processor import FrontmatterProcessor

app = typer.Typer(help="Filter files by frontmatter data")
console = Console()


def should_skip_dir(dir_name: str) -> bool:
    """Check if directory should be skipped."""
    skip_patterns = [
        lambda d: d.startswith("."),  # Hidden directories
        lambda d: d in ("venv", ".venv", "env", ".env"),  # Virtual environments
        lambda d: d == "__pycache__",  # Python cache
        lambda d: d == "node_modules",  # Node modules
        lambda d: d.startswith("_"),  # Jekyll-style directories
    ]
    return any(pattern(dir_name) for pattern in skip_patterns)


def matches_tags(metadata: dict, required_tags: List[str]) -> bool:
    """Check if metadata contains all required tags."""
    if not required_tags:
        return True

    file_tags = metadata.get("tags", [])
    if not isinstance(file_tags, list):
        file_tags = [file_tags] if file_tags else []

    # Convert to lowercase for case-insensitive comparison
    file_tags_lower = [str(tag).lower() for tag in file_tags]
    required_tags_lower = [tag.lower() for tag in required_tags]

    # All required tags must be present (AND logic)
    return all(tag in file_tags_lower for tag in required_tags_lower)


def matches_field_value(metadata: dict, field: str, value: Any, operator: str = "equals") -> bool:
    """Check if a field matches a value with the specified operator."""
    if field not in metadata:
        return False

    field_value = metadata[field]

    if operator == "equals":
        return str(field_value).lower() == str(value).lower()
    elif operator == "contains":
        return str(value).lower() in str(field_value).lower()
    elif operator == "in":
        # Check if field_value is in the list of values
        if isinstance(value, list):
            field_value_str = str(field_value).lower()
            return any(field_value_str == str(v).lower() for v in value)
        return False

    return False


def matches_field_in_list(metadata: dict, field: str, values: List[str]) -> bool:
    """Check if field value is in the list of allowed values."""
    if field not in metadata:
        return False

    field_value = metadata[field]

    # Handle both single values and lists
    if isinstance(field_value, list):
        # If field is a list, check if any item is in the allowed values
        field_values_lower = [str(v).lower() for v in field_value]
        values_lower = [str(v).lower() for v in values]
        return any(fv in values_lower for fv in field_values_lower)
    else:
        # If field is a single value, check if it's in allowed values
        field_value_lower = str(field_value).lower()
        values_lower = [str(v).lower() for v in values]
        return field_value_lower in values_lower


def collect_matching_files(
    path: Path,
    depth: int,
    tags: Optional[List[str]] = None,
    field_equals: Optional[dict] = None,
    field_in: Optional[dict] = None,
) -> List[dict]:
    """Collect all files matching the filter criteria."""
    matching_files = []
    tags = tags or []
    field_equals = field_equals or {}
    field_in = field_in or {}

    for root, dirs, files in os.walk(path):
        # Filter out directories to skip
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]

        # Check depth
        level = len(Path(root).relative_to(path).parts)
        if level >= depth:
            dirs.clear()
            continue

        # Process markdown files
        for file in files:
            if file.endswith(".md"):
                filepath = Path(root) / file
                try:
                    processor = FrontmatterProcessor(filepath)
                    metadata = processor.post.metadata

                    # Check all filter conditions
                    matches = True

                    # Check tags
                    if not matches_tags(metadata, tags):
                        matches = False

                    # Check field equals conditions
                    for field, value in field_equals.items():
                        if not matches_field_value(metadata, field, value, "equals"):
                            matches = False
                            break

                    # Check field in conditions
                    for field, values in field_in.items():
                        if not matches_field_in_list(metadata, field, values):
                            matches = False
                            break

                    if matches:
                        matching_files.append({
                            "path": str(filepath),
                            "relative_path": str(filepath.relative_to(path)),
                            "frontmatter": metadata,
                        })

                except Exception as e:
                    console.print(f"[yellow]Warning: Could not process {filepath}: {e}[/yellow]")

    return matching_files


@app.command(name="show")
def filter_files(
    path: Path = typer.Argument(
        ".",
        help="Directory to search",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
    tags: Optional[List[str]] = typer.Option(
        None,
        "--tag",
        "-t",
        help="Filter by tag(s). Multiple tags use AND logic (all must be present).",
    ),
    field: Optional[List[str]] = typer.Option(
        None,
        "--field",
        "-f",
        help="Field to filter (use with --equals or --in). Format: field=value",
    ),
    field_in: Optional[List[str]] = typer.Option(
        None,
        "--in",
        help="Filter by field with IN operator. Format: field=value1,value2,value3",
    ),
    depth: int = typer.Option(
        10,
        "--depth",
        "-d",
        help="Maximum directory depth to search",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output results as JSON",
    ),
    show_frontmatter: bool = typer.Option(
        False,
        "--frontmatter",
        help="Show full frontmatter in output",
    ),
):
    """
    Filter markdown files by frontmatter criteria.

    Examples:

    # Find files with both 'prompt' and 'agent' tags
    frontmatters filter show --tag prompt --tag agent

    # Find files where category is 'ai' OR 'system'
    frontmatters filter show --in category=ai,system

    # Combine filters: files with tags 'prompt' AND 'agent' where category is in ['ai', 'system']
    frontmatters filter show --tag prompt --tag agent --in category=ai,system

    # Filter by exact field value
    frontmatters filter show --field status=published

    # Multiple field conditions
    frontmatters filter show --field status=published --in category=ai,system --tag important
    """
    # Parse field equals conditions
    field_equals = {}
    if field:
        for f in field:
            if "=" in f:
                key, value = f.split("=", 1)
                field_equals[key.strip()] = value.strip()
            else:
                console.print(f"[red]Error: Invalid field format '{f}'. Use format: field=value[/red]")
                raise typer.Exit(1)

    # Parse field in conditions
    field_in_dict = {}
    if field_in:
        for f in field_in:
            if "=" in f:
                key, values_str = f.split("=", 1)
                values = [v.strip() for v in values_str.split(",")]
                field_in_dict[key.strip()] = values
            else:
                console.print(f"[red]Error: Invalid --in format '{f}'. Use format: field=value1,value2[/red]")
                raise typer.Exit(1)

    # Collect matching files
    matching_files = collect_matching_files(
        path=path,
        depth=depth,
        tags=tags,
        field_equals=field_equals,
        field_in=field_in_dict,
    )

    # Output results
    if json_output:
        output = {
            "total": len(matching_files),
            "files": matching_files,
        }
        console.print(json.dumps(output, indent=2))
    else:
        if not matching_files:
            console.print("[yellow]No files found matching the criteria.[/yellow]")
            return

        console.print(f"\n[green]Found {len(matching_files)} matching file(s):[/green]\n")

        if show_frontmatter:
            # Show detailed view with frontmatter
            for file_info in matching_files:
                console.print(f"[bold blue]{file_info['relative_path']}[/bold blue]")
                console.print(f"  Frontmatter:")
                for key, value in file_info['frontmatter'].items():
                    console.print(f"    {key}: {value}")
                console.print()
        else:
            # Show simple table view
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("File", style="cyan")
            table.add_column("Tags", style="green")
            table.add_column("Other Fields", style="yellow")

            for file_info in matching_files:
                tags_str = ", ".join(file_info['frontmatter'].get('tags', []))
                other_fields = {k: v for k, v in file_info['frontmatter'].items() if k != 'tags'}
                other_str = ", ".join(f"{k}={v}" for k, v in other_fields.items())

                table.add_row(
                    file_info['relative_path'],
                    tags_str or "-",
                    other_str or "-",
                )

            console.print(table)
            console.print(f"\n[green]Total: {len(matching_files)} file(s)[/green]\n")


if __name__ == "__main__":
    app()
