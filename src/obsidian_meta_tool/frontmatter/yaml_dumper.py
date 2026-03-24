from typing import Optional
from pathlib import Path
from io import StringIO
import sys

from ruamel.yaml import YAML

from obsidian_meta_tool.io.read import read_lines
from obsidian_meta_tool.io.write import write_lines
from obsidian_meta_tool.utils.lines_utils import replace_lines

yaml_parser = YAML()
def dump_yaml(data: dict) -> list:
    """
    
    Converts a dictionary to a YAML string representation. The resulting YAML string is returned as a list of lines.

    :param data: The data to be converted to YAML format. It should be a dictionary where the keys are the field names and the values are the corresponding values for those fields.
    :type data: dict
    :return: The YAML string representation of the input data, returned as a list of lines. Each element in the list corresponds to a line in the YAML output.
    :rtype: list
    """
    output = StringIO()
    yaml_parser.indent(offset=2)
    yaml_parser.dump(data, output)
    data_lines = output.getvalue().splitlines()
    return data_lines


def replace_data(origin_path: Path, old_frontmatter_start: int, old_frontmatter_end: int, 
                 new_data_lines: list, goal_path: Optional[Path] = None):

    goal_path = decide_goal_path(origin_path, goal_path)

    lines = read_lines(origin_path)

    lines = replace_lines(lines, old_frontmatter_start, old_frontmatter_end, new_data_lines)

    write_lines(goal_path, lines)


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


# if __name__ == "__main__":
    #data = {'aliases': 'alias de exemplo', 'tags': ['objetivo-uso/ativo', 'mov/meta-organizacao'], 'categorias': ['[[Objetivos (Categoria)]]'], 'objetivo_tipos': ['[[Objetivos originais]]'], 'impacto': 3, 'progresso_por_foco': 10, 'prazo': None, 'fazer': None, 'status': ['[[Em-Desenvolvimento]]', '[[〰️]]'], 'progresso': 10, 'modified': datetime.datetime(2026, 2, 23, 13, 11, 13), 'created': datetime.datetime(2026, 2, 23, 13, 10, 1)}
    #print(dump_yaml(data).splitlines())