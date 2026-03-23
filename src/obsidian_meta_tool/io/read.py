from pathlib import Path

def read_lines(path: Path) -> list:
    """
    Reads the lines of a file and returns them as a list. 

    :param path: The path to the file to be read.
    :type path: Path
    :return: A list of lines read from the file.
    :rtype: list[Any]
    """
    with path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    return lines