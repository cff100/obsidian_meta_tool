from pathlib import Path

def is_markdown_file(path: Path) -> bool:
    """Checks if the file is a markdown file based on its extension."""
    return path.suffix.lower() == '.md'

