from typing import Any, Dict
from pathlib import Path
from io import StringIO

from ruamel.yaml import YAML

yaml_parser = YAML()
def dump_yaml(data: dict) -> str:
    """Returns the YAML content as a string"""
    output = StringIO()
    yaml_parser.dump(data, output)
    return output.getvalue()


def replace_data(path: Path, old_fm_start: int, old_fm_end: int, new_data: str):

    new_data = new_data.splitlines() # This is necessary to keep the line breaks in the new data, which is important for the integrity of the file. If we don't keep the line breaks, we might end up with a file that has all the frontmatter data in a single line, which would not be valid YAML and would break the file's structure.

    with path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

        lines[old_fm_start:old_fm_end + 1] = new_data

    

if __name__ == "__main__":
    data = {'aliases': 'alias de exemplo', 'tags': ['objetivo-uso/ativo', 'mov/meta-organizacao'], 'categorias': ['[[Objetivos (Categoria)]]'], 'objetivo_tipos': ['[[Objetivos originais]]'], 'impacto': 3, 'progresso_por_foco': 10, 'prazo': None, 'fazer': None, 'status': ['[[Em-Desenvolvimento]]', '[[〰️]]'], 'progresso': 10, 'modified': datetime.datetime(2026, 2, 23, 13, 11, 13), 'created': datetime.datetime(2026, 2, 23, 13, 10, 1)}
    print(dump_yaml(data).splitlines())