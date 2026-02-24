from pathlib import Path
from typing import Optional, Dict, Any
from ruamel.yaml import YAML

# ----------------------------
# Extração do frontmatter
# ----------------------------

def extract_frontmatter(path: Path) -> Optional[str]:
    """
    Extrai o bloco YAML (frontmatter) de um arquivo Markdown.
    Retorna None se não houver frontmatter válido.
    """
    with path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    if not lines or lines[0].strip() != "---":
        return None

    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "".join(lines[1:i])

    return None


# ----------------------------
# Parsing
# ----------------------------

def parse_yaml(frontmatter: str) -> Dict[str, Any]:
    """
    Converte o frontmatter YAML (string) em dicionário Python.
    """
    yaml_parser = YAML(typ="safe")
    data = yaml_parser.load(frontmatter)

    # Garante que sempre retorne dict
    return data if isinstance(data, dict) else {}


# ----------------------------
# Orquestração
# ----------------------------

def yaml_data(path: Path) -> Optional[Dict[str, Any]]:
    """
    Retorna os dados YAML de um arquivo Markdown.
    """
    frontmatter = extract_frontmatter(path)
    if frontmatter is None:
        return None

    return parse_yaml(frontmatter)


# ----------------------------
# Execução direta
# ----------------------------

if __name__ == "__main__":
    path = Path(r"C:\Caio_(fora_do_drive)\Python_Projetos\obsidian_meta_tool\data\arquivo_de_teste.md")

    data = yaml_data(path)
    print(data)






