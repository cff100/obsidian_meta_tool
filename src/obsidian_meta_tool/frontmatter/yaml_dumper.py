from typing import Optional, Dict, Any
from pathlib import Path
from io import StringIO
import re
import datetime

from ruamel.yaml import YAML


from obsidian_meta_tool.io.read import read_lines
from obsidian_meta_tool.io.write import write_lines
from obsidian_meta_tool.utils.lines_utils import replace_lines
from obsidian_meta_tool.utils.frontmatter_utils import frontmatter_line_numbers


def replace_data(origin_path: Path, new_frontmatter: Dict[str, Any], goal_path: Optional[Path] = None):
    """
    Replaces the existing frontmatter in a file with new data.

    This function reads the content of the `origin_path`, identifies the existing 
    frontmatter boundaries, replaces those lines with the YAML representation 
    of `new_frontmatter`, and writes the result to `goal_path`.

    :param origin_path: File path of the original file.
    :type origin_path: Path
    :param new_frontmatter: New frontmatter data to be inserted into the file.
    :type new_frontmatter: Dict[str, Any]
    :param goal_path: File path of the goal file. If not provided, the original file will be overwritten.
    :type goal_path: Optional[Path]    
    """

    new_frontmatter_lines = dump_yaml(new_frontmatter)

    goal_path = decide_goal_path(origin_path, goal_path)

    lines = read_lines(origin_path)

    old_frontmatter_start, old_frontmatter_end = frontmatter_line_numbers(lines)

    lines = replace_lines(lines, old_frontmatter_start, old_frontmatter_end, new_frontmatter_lines)

    write_lines(goal_path, lines)



class DatetimeWithT:
    """Datetime wrapper that forces output in ISO format with T."""
    def __init__(self, dt):
        self.dt = dt

def represent_datetime_with_t(representer, data):
    """Representative for the DatetimeWithT wrapper."""
    return representer.represent_scalar(
        'tag:yaml.org,2002:timestamp', 
        data.dt.isoformat()
    )

def prepare_datetime_with_t(data: Dict[str, Any]) -> Dict[str, Any]:
    """Replace the values of the special keys with the wrapper."""
    for key in ['created', 'modified']:
        if key in data and isinstance(data[key], datetime.datetime):
            data[key] = DatetimeWithT(data[key])
    return data


yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(offset=2)
yaml.representer.add_representer(DatetimeWithT, represent_datetime_with_t)

def dump_yaml(data: Dict[str, Any]) -> list:
    """
    
    Converts a dictionary to a YAML string representation. The resulting YAML string is returned as a list of lines.

    :param data: The data to be converted to YAML format. It should be a dictionary where the keys are the field names and the values are the corresponding values for those fields.
    :type data: Dict[str, Any]
    :return: The YAML string representation of the input data, returned as a list of lines. Each element in the list corresponds to a line in the YAML output.
    :rtype: list
    """

    data = prepare_datetime_with_t(data)

    output = StringIO()
    yaml.dump(data, output)

    lines = output.getvalue().splitlines(keepends=True)
    lines = replace_single_with_double_quotes(lines)

    return lines


def decide_goal_path(origin_path: Path, goal_path: Optional[Path] = None) -> Path:
    """
    Decides the goal path for the output file. 
    If the `goal_path` is provided, it will be used as the output path. 
    If the `goal_path` is not provided (i.e., it is `None`), the `origin_path` will be used as the output path.

    :param origin_path: The original path of the file that is being processed. This path will be used as the output path if the `goal_path` is not provided.
    :type origin_path: Path
    :param goal_path: The desired path for the output file.
    :return: The path that will be used for the output file. It will be the `goal_path` if it is provided, or the `origin_path` if the `goal_path` is not provided.
    :rtype: Path
    """
    if goal_path == None:
        goal_path = origin_path

    return goal_path

def replace_single_with_double_quotes(lines: list) -> list:
    """ Replace '[[...]]' with "[[...]]" """
    for i, line in enumerate(lines): 
        lines[i] = re.sub(r"'(\[\[.*?\]\])'", r'"\1"', line)
    return lines
