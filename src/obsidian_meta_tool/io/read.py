from pathlib import Path

def read_lines(path: Path) -> list:
    """
    Reads the lines of a file and returns them as a list. 

    :param path: The path to the file to be read.
    :type path: Path
    :return: A list of lines read from the file.
    :rtype: list[Any]
    """
    
    # if not path.is_file():
    #     print(f"Not a file (is directory or doesn't exist): {path}")
    #     return []
    
    try:
        with path.open("r", encoding="utf-8") as file:
            lines = file.readlines()
    except PermissionError:
        print(f"Access denied: {path}")
        lines = []
    except UnicodeDecodeError:
        print(f"Encoding error in: {path}")
        lines = []

    return lines