from pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum

from ruamel.yaml import YAML, YAMLError

from obsidian_meta_tool.utils.frontmatter_utils import frontmatter_line_numbers
from obsidian_meta_tool.error_classes import frontmatter_errors as fe
from obsidian_meta_tool.io.read import read_lines


class FrontmatterStatus(Enum):
    """
    Enum representing the status of the frontmatter in a Markdown file.

    :var VALID: Status indicating that the frontmatter is valid and can be parsed.
    :vartype VALID: Literal['valid']
    :var MISSING: Status indicating that the frontmatter is missing from the file.
    :vartype MISSING: Literal['missing']
    :var BROKEN: Status indicating that the frontmatter is present but not properly closed, making it unparseable.
    :vartype BROKEN: Literal['broken']
    :var EMPTY: Status indicating that the frontmatter is present but empty.
    :vartype EMPTY: Literal['empty']
    :var EMPTY_FILE: Status indicating that the file is empty.
    :vartype EMPTY_FILE: Literal['empty_file']
    """
    VALID = "valid"
    MISSING = "missing"
    BROKEN = "broken"
    EMPTY = "empty"
    EMPTY_FILE = "empty_file"


def retrieve_yaml_data(path: Path) -> tuple[FrontmatterStatus, Optional[Dict[str, Any]]]:
    """
    Returns the YAML data from a Markdown file.

    :param path: Markdown file path. Pressuposed to be a valid path to a Markdown file.
    :type path: Path
    :return: A tuple with the status of the frontmatter and the frontmatter data (if valid).
        The status can be "valid", "missing", "broken", "empty" or "empty_file". If the frontmatter is not valid, the second element of the tuple will be None.
    :rtype: tuple[FrontmatterStatus, Optional[Dict[str, Any]]]
    """

    status, frontmatter = extract_frontmatter(path)
    data = retrieve_existent_frontmatter(status, frontmatter)

    return status, data


def extract_frontmatter(path: Path) -> tuple[FrontmatterStatus, Optional[str]]:
    """
    Extracts the frontmatter from a Markdown file. 
    Returns a tuple with the status of the frontmatter and the frontmatter string (if valid). 
    The status can be "valid", "missing", "broken", "empty" or "empty_file".

    :param path: Markdown file path. Pressuposed to be a valid path to a Markdown file.
    :return: A tuple with the status of the frontmatter and the frontmatter string (if valid).
        If not valid, the second element of the tuple will be None.
    :rtype: tuple[FrontmatterStatus, Optional[str]]
    """

    lines = read_lines(path)

    #print(f"Lines: {lines}") # For debugging purposes

    try:
        start, end = frontmatter_line_numbers(lines)
        return FrontmatterStatus.VALID, "".join(lines[start:end+1])
    
    except fe.NoLinesError:
        return FrontmatterStatus.EMPTY_FILE, None
    
    except fe.NoFrontmatterError:
        return FrontmatterStatus.MISSING, None

    except fe.UnclosedFrontmatterError:
        return FrontmatterStatus.BROKEN, None

    except fe.EmptyFrontmatterError:
        return FrontmatterStatus.EMPTY, None

    
def retrieve_existent_frontmatter(status: FrontmatterStatus, frontmatter: str | None) -> Optional[Dict[str, Any]]:
    """
    Returns the YAML data from a Markdown file.

    :param status: Status of the frontmatter.
    :type status: FrontmatterStatus
    :param frontmatter: Frontmatter string. `None` if the frontmatter is not valid.
    :type frontmatter: Optional[str]
    :return: Frontmatter dictionary or None if the `frontmatter` is not valid.
    :rtype: Dict[str, Any]
    """

    if status in (FrontmatterStatus.VALID, FrontmatterStatus.EMPTY):
        return parse_yaml(frontmatter)
    else:
        return None
    

yaml_parser = YAML(typ="safe")
def parse_yaml(frontmatter: Optional[str]) -> Dict[str, Any]:
    """
    Converts the YAML frontmatter (string) into a Python dictionary.

    :param frontmatter: File frontmatter. `None` if the frontmatter is None (empty).
    :type frontmatter: Optional[str]
    :return: Frontmatter dictionary or empty dictionary if the `frontmatter` is None.
    :rtype: Dict[str, Any]
    """

    if frontmatter is None:
        return {}
 
    try:
        data = yaml_parser.load(frontmatter)
        return data
    except YAMLError:
        return {}