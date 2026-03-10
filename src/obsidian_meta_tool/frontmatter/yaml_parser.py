from pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum

from ruamel.yaml import YAML, YAMLError

from obsidian_meta_tool.utils.frontmatter_utils import frontmatter_line_numbers
from obsidian_meta_tool.error_classes import frontmatter_errors as fe


class FrontmatterStatus(Enum):
    VALID = "valid"
    MISSING = "missing"
    BROKEN = "broken"
    EMPTY = "empty"
    EMPTY_FILE = "empty_file"


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

    with path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

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

    

yaml_parser = YAML(typ="safe")
def parse_yaml(frontmatter: Optional[str]) -> Dict[str, Any]:
    """
    Converts the YAML frontmatter (string) into a Python dictionary.

    :param frontmatter: File frontmatter. `None` if the frontmatter is None (empty).
    :type frontmatter: Optional[str]
    :return: Frontmatter dictionary.
    :rtype: Dict[str, Any]
    """

    if frontmatter is None:
        return {}
 
    try:
        data = yaml_parser.load(frontmatter)
    except YAMLError:
        return {}

    if isinstance(data, dict):
        return data

    return {}



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

    if status in (FrontmatterStatus.VALID, FrontmatterStatus.EMPTY):
        return status, parse_yaml(frontmatter)

    return status, None


if __name__ == "__main__":
    path = Path(r"C:\Caio_(fora_do_drive)\Python_Projetos\
                obsidian_meta_tool\tests\test_files\
                common_file_1.md")

    data = retrieve_yaml_data(path)
    print(f"Yaml_data: {data}")





