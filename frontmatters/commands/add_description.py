import os
import typer
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from frontmatters.core.processor import FrontmatterProcessor

app = typer.Typer()


def should_skip_dir(dir_name: str) -> bool:
    """Check if directory should be skipped"""
    skip_patterns = [
        # Hidden directories
        lambda d: d.startswith("."),
        # Python virtual environments
        lambda d: d in ("venv", ".venv", "env", ".env"),
        # Cache directories
        lambda d: d in ("__pycache__", ".pytest_cache", ".ruff_cache"),
        # Node.js
        lambda d: d == "node_modules",
        # Build directories
        lambda d: d in ("build", "dist", ".next", ".nuxt"),
        # Version control
        lambda d: d in (".git", ".svn", ".hg"),
        # IDE directories
        lambda d: d in (".vscode", ".idea"),
        # OS-specific
        lambda d: d in ("__MACOSX", ".DS_Store"),
        # Common development directories
        lambda d: d in ("target", ".gradle", ".mvn"),
    ]
    return any(pattern(dir_name) for pattern in skip_patterns)


def read_gitignore(path: Path) -> set:
    """Read .gitignore patterns from directory"""
    gitignore_path = path / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path, "r", encoding="utf-8") as f:
            return set(
                line.strip() for line in f if line.strip() and not line.startswith("#")
            )
    return set()


def get_description(content, api_key, model="moonshotai/kimi-k2"):
    """Generate description using OpenRouter API"""
    truncated = content[:2000] + "..." if len(content) > 2000 else content

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": f"Write a 1-3 sentence description of this document. Be succinct and focus on it from a categorical or classification perspective. If you can't be certain just write 'unknown'. Here is the document:\n\n{truncated}",
                }
            ],
            "max_tokens": 100,
        },
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def process_single_file(filepath: Path, api_key: str, force: bool, model: str):
    processor = FrontmatterProcessor(filepath)

    if processor.has_frontmatter("description") and not force:
        print(f"Skipping {filepath} - description exists")
        return

    if not processor.content.strip():
        print(f"Skipping {filepath} - no content")
        return

    print(f"Processing {filepath}")
    description = get_description(processor.content, api_key, model)
    processor.update_frontmatter("description", description)


def find_files_missing_description(path: Path, depth: int) -> List[Dict[str, Any]]:
    """Find all markdown files missing descriptions"""
    files_missing = []

    for root, dirs, files in os.walk(path):
        # Filter out directories to skip
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]

        level = len(Path(root).relative_to(path).parts)
        if level >= depth:
            dirs.clear()
            continue

        for file in files:
            if file.endswith(".md"):
                filepath = Path(root) / file
                try:
                    processor = FrontmatterProcessor(filepath)

                    if not processor.has_frontmatter("description"):
                        # Get file stats
                        stat = filepath.stat()
                        last_modified = datetime.fromtimestamp(stat.st_mtime)

                        # Extract metadata
                        metadata = processor.post.metadata

                        files_missing.append(
                            {
                                "path": str(filepath.absolute()),
                                "vault": str(path.absolute()),
                                "domain": metadata.get("domain", ""),
                                "tags": metadata.get("tags", []),
                                "last_modified": last_modified,
                            }
                        )
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

    # Sort by last modified date (newest first)
    files_missing.sort(key=lambda x: x["last_modified"], reverse=True)
    return files_missing


@app.command()
def missing(
    path: Path = typer.Argument(..., help="Directory to search"),
    depth: int = typer.Option(
        10, "--depth", "-d", help="Max depth for directory traversal"
    ),
):
    """
    List all markdown files missing descriptions in a tabular format.
    """
    console = Console()

    files_missing = find_files_missing_description(path, depth)

    if not files_missing:
        console.print("[green]All files have descriptions![/green]")
        return

    # Create table
    table = Table(
        title="Files Missing Descriptions",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("File Path", style="cyan")
    table.add_column("Vault", style="magenta")
    table.add_column("Domain", style="yellow")
    table.add_column("Tags", style="green")
    table.add_column("Last Modified", style="red")

    for file_info in files_missing:
        tags_str = ", ".join(file_info["tags"]) if file_info["tags"] else ""
        last_modified_str = file_info["last_modified"].strftime("%Y-%m-%d %H:%M")

        table.add_row(
            file_info["path"],
            file_info["vault"],
            file_info["domain"],
            tags_str,
            last_modified_str,
        )

    console.print(table)
    console.print(
        f"\n[bold]Total files missing descriptions: {len(files_missing)}[/bold]"
    )


@app.command()
def add(
    path: Path = typer.Argument(..., help="File or directory to process"),
    depth: int = typer.Option(
        10, "--depth", "-d", help="Max depth for directory traversal"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Overwrite existing descriptions"
    ),
    model: str = typer.Option(
        "moonshotai/kimi-k2", "--model", "-m", help="OpenRouter model to use"
    ),
):
    """
    Adds descriptions to markdown files using an AI model.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise typer.Exit("OPENROUTER_API_KEY not found")

    if path.is_file() and path.suffix == ".md":
        try:
            process_single_file(path, api_key, force, model)
        except Exception as e:
            print(f"Error processing {path}: {e}")
    elif path.is_dir():
        for root, dirs, files in os.walk(path):
            # Filter out directories to skip
            dirs[:] = [d for d in dirs if not should_skip_dir(d)]

            level = len(Path(root).relative_to(path).parts)
            if level >= depth:
                dirs.clear()
                continue

            for file in files:
                if file.endswith(".md"):
                    filepath = Path(root) / file
                    try:
                        process_single_file(filepath, api_key, force, model)
                    except Exception as e:
                        print(f"Error processing {filepath}: {e}")
    else:
        print(f"Invalid path: {path}")
