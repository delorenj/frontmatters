import os
import typer
import requests
from pathlib import Path
from frontmatters.core.processor import FrontmatterProcessor

app = typer.Typer()

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


@app.command()
def add(
    path: Path = typer.Argument(..., help="File or directory to process"),
    depth: int = typer.Option(10, "--depth", "-d", help="Max depth for directory traversal"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing descriptions"),
    model: str = typer.Option("moonshotai/kimi-k2", "--model", "-m", help="OpenRouter model to use"),
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