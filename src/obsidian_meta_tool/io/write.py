from pathlib import Path

def write_lines(path: Path, lines: list) -> None:
    """
    Writes a list of lines to a file. 
    Each line in the list should include a newline character at the end.
    Erases the previous content of the file.

    :param path: The path to the file to be written.
    :type path: Path
    :param lines: The list of lines to be written to the file.
    :type lines: list
    """
    with path.open("w", encoding="utf-8") as file:
        file.writelines(lines)

