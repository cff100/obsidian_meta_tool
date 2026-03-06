from pathlib import Path
from typing import Dict, Any

from ruamel.yaml import YAML

from obsidian_meta_tool.utils.frontmatter_utils import frontmatter_line_numbers



# ----------------------------
# Frontmatter extraction
# ----------------------------

def extract_frontmatter(path: Path) -> str:
    """
    Extracts the YAML frontmatter block from a Markdown file via its path.

    :param path: Markdown file path.
    :type path: Path
    :return: File frontmatter.
    :rtype: str
    """

    with path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    # print(f"Lines: {lines}")

    start, end = frontmatter_line_numbers(lines)
    return "".join(lines[start:end+1])



# ----------------------------
# Parsing
# ----------------------------

def parse_yaml(frontmatter: str) -> Dict[str, Any]:
    """
    Converts the YAML frontmatter (string) into a Python dictionary.

    :param frontmatter: File frontmatter.
    :type frontmatter: str
    :return: Frontmatter dictionary.
    :rtype: Dict[str, Any]
    """

    yaml_parser = YAML(typ="safe")
    data = yaml_parser.load(frontmatter)

    return data if isinstance(data, dict) else {}


# ----------------------------
# Orchestration
# ----------------------------

def yaml_data(path: Path) -> Dict[str, Any]:
    """
    Returns the YAML data from a Markdown file.
    """

    frontmatter = extract_frontmatter(path)
    return parse_yaml(frontmatter)


# ----------------------------
# Direct execution
# ----------------------------

if __name__ == "__main__":
    path = Path(r"C:\Caio_(fora_do_drive)\Python_Projetos\obsidian_meta_tool\data\arquivo_de_teste_1.md")


    # frontmatter = extract_frontmatter(path)
    # print(frontmatter)

    # data = parse_yaml(frontmatter)
    # print(data)

    data = yaml_data(path)
    print(f"Yaml_data: {data}")





