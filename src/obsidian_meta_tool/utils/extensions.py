
from pathlib import Path


def is_md(path: Path) -> bool:

    return path.suffix == ".md"

def is_text_file(path: Path) -> bool:

    if path.is_dir:
        print("A")
        return False
    elif path.suffix not in [".md", ".txt"]:
        print("B")
        return False
    else: 
        print("C")
        return True