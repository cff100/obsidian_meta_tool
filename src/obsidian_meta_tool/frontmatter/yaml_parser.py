from pathlib import Path
from typing import Dict, Any

from ruamel.yaml import YAML

from obsidian_meta_tool.utils.frontmatter_utils import frontmatter_line_numbers
from obsidian_meta_tool.error_classes import frontmatter_errors as fe



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

    print(f"Lines: {lines}") # For debugging purposes

    try:
        start, end = frontmatter_line_numbers(lines)
        return "".join(lines[start:end+1])
    except (fe.NoFrontmatterError, fe.NoLinesError, fe.UnclosedFrontmatterError, fe.EmptyFrontmatterError):
        return ""



def parse_yaml(frontmatter: str) -> Dict[str, Any]:
    """
    Converts the YAML frontmatter (string) into a Python dictionary.

    :param frontmatter: File frontmatter.
    :type frontmatter: str
    :return: Frontmatter dictionary.
    :rtype: Dict[str, Any]
    """

    yaml_parser = YAML(typ="safe")
    try:
        data = yaml_parser.load(frontmatter)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}



def yaml_data(path: Path) -> Dict[str, Any]:
    """
    Returns the YAML data from a Markdown file.
    """

    frontmatter = extract_frontmatter(path)
    return parse_yaml(frontmatter)


if __name__ == "__main__":
    path = Path(r"C:\Caio_(fora_do_drive)\Python_Projetos\obsidian_meta_tool\tests\test_files\common_file_1.md")
    #path = Path(r"C:\Caio_(fora_do_drive)\Python_Projetos\obsidian_meta_tool\tests\test_files\empty_file.md")

    # frontmatter = extract_frontmatter(path)
    # print(frontmatter)

    # data = parse_yaml(frontmatter)
    # print(data)

    data = yaml_data(path)
    print(f"Yaml_data: {data}")





