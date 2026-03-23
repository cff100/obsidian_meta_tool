from typing import Optional
from pathlib import Path
from io import StringIO

from ruamel.yaml import YAML

from obsidian_meta_tool.io.read import read_lines
from obsidian_meta_tool.utils.lines_utils import split_lines

yaml_parser = YAML()
def dump_yaml(data: dict) -> str:
    """Returns the YAML content as a string"""
    output = StringIO()
    yaml_parser.dump(data, output)
    return output.getvalue()


def replace_data(origin_path: Path, old_fm_start: int, old_fm_end: int, new_data: str, goal_path: Optional[Path] = None):

    if goal_path == None:
        goal_path = origin_path

    lines = read_lines(origin_path)

    lines = split_lines(old_fm_start, old_fm_end, lines, new_data.splitlines())

    with goal_path.open("w", encoding="utf-8") as file:
        file.writelines(lines)



# if __name__ == "__main__":
    #data = {'aliases': 'alias de exemplo', 'tags': ['objetivo-uso/ativo', 'mov/meta-organizacao'], 'categorias': ['[[Objetivos (Categoria)]]'], 'objetivo_tipos': ['[[Objetivos originais]]'], 'impacto': 3, 'progresso_por_foco': 10, 'prazo': None, 'fazer': None, 'status': ['[[Em-Desenvolvimento]]', '[[〰️]]'], 'progresso': 10, 'modified': datetime.datetime(2026, 2, 23, 13, 11, 13), 'created': datetime.datetime(2026, 2, 23, 13, 10, 1)}
    #print(dump_yaml(data).splitlines())