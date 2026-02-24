import sys
import datetime
from typing import Any

from ruamel.yaml import YAML

def dump_yaml(data: dict) -> Any:

    yaml_parser = YAML()
    return yaml_parser.dump(data, sys.stdout)

if __name__ == "__main__":
    data = {'aliases': 'alias de exemplo', 'tags': ['objetivo-uso/ativo', 'mov/meta-organizacao'], 'categorias': ['[[Objetivos (Categoria)]]'], 'objetivo_tipos': ['[[Objetivos originais]]'], 'impacto': 3, 'progresso_por_foco': 10, 'prazo': None, 'fazer': None, 'status': ['[[Em-Desenvolvimento]]', '[[〰️]]'], 'progresso': 10, 'modified': datetime.datetime(2026, 2, 23, 13, 11, 13), 'created': datetime.datetime(2026, 2, 23, 13, 10, 1)}
    print(dump_yaml(data))