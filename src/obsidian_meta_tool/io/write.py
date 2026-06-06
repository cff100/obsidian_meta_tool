from pathlib import Path

def write_lines(
    path: Path, 
    lines: list[str], 
    create_parents: bool = True, 
    overwrite_only: bool = True
) -> None:
    """
    Writes a list of string lines to a file, replacing its current content.

    :param path: The destination path where the file will be written.
    :type path: Path
    :param lines: The list of string lines to write into the file.
    :type lines: list[str]
    :param create_parents: If True, automatically creates missing parent directories. Defaults to True.
    :type create_parents: bool
    :param overwrite_only: If True, restricts operation to existing files only. Raises an error if the file does not exist.
    :type overwrite_only: bool
    :return: None
    :rtype: NoneType
    :raises FileNotFoundError: If overwrite_only is True and the target file does not exist.
    :raises PermissionError: If write access to the destination is denied by the OS.
    :raises IsADirectoryError: If the provided path points to a directory instead of a file.
    """
    if overwrite_only and not path.is_file():
        raise FileNotFoundError(f"Target file does not exist for overwrite: {path}")

    if create_parents:
        path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        file.writelines(lines)