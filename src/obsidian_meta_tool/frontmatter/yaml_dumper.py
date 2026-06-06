import copy
import datetime
from io import StringIO
from pathlib import Path
import re
from typing import Any, Optional, cast

from ruamel.yaml import YAML

from obsidian_meta_tool.config.constants import FRONT_MATTER_TIMESTAMPS_PLUGIN_NAMES
from obsidian_meta_tool.io.read import read_lines
from obsidian_meta_tool.io.write import write_lines
from obsidian_meta_tool.utils.lines_utils import replace_lines


class DatetimeWithT:
    """Datetime wrapper that forces output in ISO format with T."""
    def __init__(self, dt: datetime.datetime):
        self.dt = dt


def represent_datetime_with_t(representer, data: DatetimeWithT):
    """Representative for the DatetimeWithT wrapper."""
    return representer.represent_scalar(
        'tag:yaml.org,2002:timestamp', 
        data.dt.isoformat()
    )


def prepare_datetime_with_t(data: dict[str, Any]) -> dict[str, Any]:
    """
    Creates a deep copy of the dictionary and replaces datetime values 
    for special tracking keys with the DatetimeWithT wrapper.

    :param data: The original frontmatter data dictionary.
    :type data: dict[str, Any]
    :return: A modified copy of the dictionary safely wrapped for YAML serialization.
    :rtype: dict[str, Any]
    """
    data_copy = copy.deepcopy(data)
    for key in FRONT_MATTER_TIMESTAMPS_PLUGIN_NAMES:
        if key in data_copy and isinstance(data_copy[key], datetime.datetime):
            data_copy[key] = DatetimeWithT(data_copy[key])
    return data_copy


# Initialize and configure the global YAML object
yaml = YAML()
yaml.preserve_quotes = True
# cast(Any, yaml).default_style = '"'  
yaml.indent(offset=2)
yaml.representer.add_representer(DatetimeWithT, represent_datetime_with_t)


def replace_single_with_double_quotes(lines: list[str]) -> list[str]:
    """
    Fixes Obsidian Wikilinks and Timestamps enclosed by single quotes 
    or unquoted into proper double quotes, ensuring Obsidian compatibility.
    """
    for i, line in enumerate(lines): 
        # 1. Corrige Wikilinks com aspas simples: '[[Link]]' -> "[[Link]]"
        line = re.sub(r"'(\[\[.*?\]\])'", r'"\1"', line)
        
        # 2. Garante que se o ruamel gerou o timestamp sem aspas, nós adicionamos aspas duplas
        # Ex: dt_key: 2026-06-06T15:30:45 -> dt_key: "2026-06-06T15:30:45"
        # Captura a chave e o valor do timestamp ISO
        line = re.sub(r"(\w+):\s*(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", r'\1: "\2"', line)
        
        lines[i] = line
    return lines


def dump_yaml(data: dict[str, Any]) -> list[str]:
    """
    Converts a dictionary into a YAML string representation returned as a list of lines.

    :param data: The data dictionary to convert into YAML layout.
    :type data: dict[str, Any]
    :return: A list where each element represents a single line of raw YAML output.
    :rtype: list[str]
    """
    serializable_data = prepare_datetime_with_t(data)

    output = StringIO()
    yaml.dump(serializable_data, output)

    lines = output.getvalue().splitlines(keepends=True)
    lines = replace_single_with_double_quotes(lines)

    return lines


def decide_goal_path(origin_path: Path, goal_path: Optional[Path] = None) -> Path:
    """
    Resolves the targeted path for saving the output file.

    :param origin_path: The file path of the original input markdown note.
    :type origin_path: Path
    :param goal_path: Optional targeted destination path. If None, it targets origin_path.
    :type goal_path: Optional[Path]
    :return: Resolved destination path where files will be written.
    :rtype: Path
    """
    return origin_path if goal_path is None else goal_path


def replace_data(
    origin_path: Path, 
    new_frontmatter: dict[str, Any], 
    fm_start: int, 
    fm_end: int, 
    goal_path: Optional[Path] = None
) -> None:
    """
    Replaces the existing frontmatter in a file using pre-calculated line indices.

    This function reads the content of `origin_path`, replaces the lines inside the
    specified boundary (`fm_start` to `fm_end`) with the new YAML representation, 
    and writes the updated content to `goal_path`.

    :param origin_path: File path of the original file.
    :type origin_path: Path
    :param new_frontmatter: New frontmatter data to be inserted into the file.
    :type new_frontmatter: dict[str, Any]
    :param fm_start: Pre-calculated start line index of the frontmatter content.
    :type fm_start: int
    :param fm_end: Pre-calculated end line index of the frontmatter content.
    :type fm_end: int
    :param goal_path: File path of the goal file. If not provided, the original file will be overwritten.
    :type goal_path: Optional[Path]    
    """
    # 1. Generate the new raw YAML lines
    new_frontmatter_lines = dump_yaml(new_frontmatter)
    resolved_goal_path = decide_goal_path(origin_path, goal_path)

    # 2. Read the full file lines
    lines = read_lines(origin_path)

    # 3. Use the pre-calculated indices instantly without re-scanning the file
    updated_lines = replace_lines(lines, fm_start, fm_end, new_frontmatter_lines)

    # 4. Save the file
    write_lines(resolved_goal_path, updated_lines, create_parents = False)