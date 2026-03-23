from pathlib import Path


def write_lines(path: Path, lines: list) -> None:
    with path.open("w", encoding="utf-8") as file:
        file.writelines(lines)

