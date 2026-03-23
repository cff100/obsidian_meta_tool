from pathlib import Path

def read_lines(path: Path) -> list:
    with path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    return lines