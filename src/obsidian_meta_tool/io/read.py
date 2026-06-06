from pathlib import Path

def read_lines(path: Path, without_newline_character: bool = False) -> list[str]:
    """
    Reads the lines of a file and returns them as a list of strings.

    :param path: The path to the file to be read.
    :type path: Path
    :param without_newline_character: If True, removes trailing newline characters (\\r, \\n) from the end of each line.
    :type without_newline_character: bool
    :return: A list of string lines read from the file.
    :rtype: list[str]
    :raises FileNotFoundError: If the file does not exist at the specified path.
    :raises PermissionError: If read access to the file is denied by the OS.
    :raises UnicodeDecodeError: If the file content cannot be decoded using UTF-8.
    """
    with path.open("r", encoding="utf-8") as file:
        if without_newline_character:
            return file.read().splitlines()
        return file.readlines()


def read_file_paths(path: Path) -> list[Path]:
    """
    Reads a text file containing file paths (one per line) and returns them as a list of Path objects.

    This function automatically handles trailing newline characters, sanitizes the text, 
    and filters out any empty lines to prevent the creation of invalid or empty Path instances.

    :param path: The path to the text file containing the list of file paths.
    :type path: Path
    :return: A list of valid Path objects extracted from the file lines.
    :rtype: list[Path]
    :raises FileNotFoundError: If the path configuration file does not exist.
    :raises PermissionError: If read access to the file is denied by the OS.
    :raises UnicodeDecodeError: If the file content cannot be decoded using UTF-8.
    """
    lines = read_lines(path, without_newline_character=True)
    return [Path(line) for line in lines if line.strip()]