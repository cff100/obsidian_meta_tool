from typing import Any, Optional
from enum import Enum
from ruamel.yaml import YAML, YAMLError

from obsidian_meta_tool.errors import frontmatter_errors as fe

class FrontmatterStatus(Enum):
    """
    Enum representing the status of the frontmatter in a Markdown file.

    :var VALID: Status indicating that the frontmatter is valid and can be parsed.
    :vartype VALID: Literal['valid']
    :var MISSING: Status indicating that the frontmatter is missing from the file.
    :vartype MISSING: Literal['missing']
    :var BROKEN: Status indicating that the frontmatter is present but not properly closed or contains invalid YAML syntax (e.g., incorrect indentation, malformed braces). 
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


def frontmatter_line_numbers(file_lines: list[str]) -> tuple[int, int]:
    """
    Finds the start and end line indices of the YAML frontmatter content.
    The indices returned correspond to the actual data lines, excluding the '---' markers.

    :param file_lines: A list whose elements are the lines of a file.
    :type file_lines: list[str]
    :return: Index of the start and end lines, respectively, of the frontmatter (does not consider the '---' markers).
    :rtype: tuple[int, int]
    :raises NoLinesError: If the file has no lines to process.
    :raises NoFrontmatterError: If the file does not start with a '---' marker.
    :raises UnclosedFrontmatterError: If the frontmatter is not properly closed (missing closing '---' marker).
    :raises EmptyFrontmatterError: If the frontmatter is empty (No values between the markers '---').
    """
    if not file_lines:
        raise fe.NoLinesError("The file has no lines to process.")
    
    if file_lines[0].strip() != "---":
        raise fe.NoFrontmatterError("There is no frontmatter in this file.")
    
    fm_start = 1
    fm_end: Optional[int] = None

    for i in range(1, len(file_lines)):
        if file_lines[i].strip() == "---":
            fm_end = i - 1
            break
    
    if fm_end is None:
        raise fe.UnclosedFrontmatterError("The frontmatter of the file is not properly closed (missing closing '---' marker).") 

    if fm_end < fm_start:
        raise fe.EmptyFrontmatterError("The frontmatter is empty (No values between the markers '---').")

    return fm_start, fm_end


# Instantiated outside to avoid memory reallocation on each function call.
yaml_parser = YAML(typ="safe")


def retrieve_yaml_data(note_lines: list[str]) -> tuple[FrontmatterStatus, Optional[dict[str, Any]], Optional[int], Optional[int]]:
    """
    Extracts, parses, and returns the YAML data along with its status and line indices.

    :param note_lines: A list whose elements are the lines of a Markdown file.
    :type note_lines: list[str]
    :return: A tuple containing (Status, Data, Start_Line_Index, End_Line_Index).
             If the status is 'VALID' or 'EMPTY', indices are returned. 
             For other statuses, Data, Start, and End will be None (or empty dict for EMPTY).
    :rtype: tuple[FrontmatterStatus, Optional[dict[str, Any]], Optional[int], Optional[int]]
    """

    try:
        start, end = frontmatter_line_numbers(note_lines)
        frontmatter_str = "".join(note_lines[start:end+1])
        
        try:
            data = yaml_parser.load(frontmatter_str)
            # If the YAML file is valid but returns None (e.g., file with only comments inside separators)
            return FrontmatterStatus.VALID, (data if data is not None else {}), start, end
        except YAMLError:
            return FrontmatterStatus.BROKEN, None, start, end

    except fe.NoLinesError:
        return FrontmatterStatus.EMPTY_FILE, None, None, None
    
    except fe.NoFrontmatterError:
        return FrontmatterStatus.MISSING, None, None, None

    except fe.UnclosedFrontmatterError:
        return FrontmatterStatus.BROKEN, None, None, None

    except fe.EmptyFrontmatterError:
        # The start will be 1 and the end will be 0 (indicating that there are no data lines between them).
        return FrontmatterStatus.EMPTY, {}, 1, 0