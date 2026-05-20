from pathlib import Path
from typing import Any, Optional
from enum import Enum
import re


from obsidian_meta_tool.frontmatter.yaml_parser import retrieve_yaml_data
from obsidian_meta_tool.io.read import read_lines

class CategoriesNames(Enum):
    NOTE_PATH = "note_path"
    NOTE_EXTENSION = "note_extension"
    NOTE_FILENAME = "note_filename"
    NOTE_INITIAL_FOLDER_NAME = "note_initial_folder_name"
    NOTE_FRONTMATTER_STATUS = "note_frontmatter_status"
    NOTE_FRONTMATTER = "note_frontmatter"
    NOTE_BODY_TAGS = "note_body_tags",
    NOTE_OUTGOING_LINKS = "note_outgoing_links"


def get_all_categories(note_path: Path, vault_path: Path) -> dict[CategoriesNames, Any]:
    """
    Get all categories from a note.

    :param note_path: Path to the note.
    :type note_path: Path
    :param vault_path: Path to the vault.
    :type vault_path: Path
    :return: A dictionary with all categories.
    :rtype: dict[CategoriesNames, Any]
    """

    note_lines = read_lines(note_path)

    note_extension = get_extension(note_path)
    note_filename = get_filename(note_path)
    initial_folder_name = get_initial_folder_name(note_path, vault_path)
    frontmatter_status, frontmatter = retrieve_yaml_data(note_lines)
    note_body_tags = get_body_tags(note_lines)
    note_outgoing_links = get_outgoing_links(note_lines)
    
    categories = {
        CategoriesNames.NOTE_PATH: note_path, 
        CategoriesNames.NOTE_EXTENSION: note_extension, 
        CategoriesNames.NOTE_FILENAME: note_filename, 
        CategoriesNames.NOTE_INITIAL_FOLDER_NAME: initial_folder_name, 
        CategoriesNames.NOTE_FRONTMATTER_STATUS: frontmatter_status.value, 
        CategoriesNames.NOTE_FRONTMATTER: frontmatter,
        CategoriesNames.NOTE_BODY_TAGS: note_body_tags,
        CategoriesNames.NOTE_OUTGOING_LINKS: note_outgoing_links
        }

    return categories


def get_extension(note_path: Path) -> str:

    note_extension = note_path.suffix
    return note_extension


def get_filename(note_path: Path) -> str:

    note_filename = note_path.stem
    return note_filename


def get_initial_folder_name(note_path: Path, vault_path: Path) -> str:

    initial_folder_name = note_path.relative_to(vault_path).parts[0]
    return initial_folder_name


def get_body_tags(note_lines: list[str]) -> Optional[list[str]]:

    body_tags = []
    for line in note_lines:
        if "#" in line:
            expressions = line.split()
            for expression in expressions:
                if expression.startswith("#"):
                    tag = expression[1:]
                    body_tags.append(tag)
        
    if not body_tags:
        return None

    body_tags = list(set(body_tags))
    return body_tags


def get_outgoing_links(note_lines: list[str]) -> Optional[list[str]]:

    outgoing_links = []
    pattern = r"\[\[([^|\]]+)(?:\|[^\]]+)?\]\]"

    for line in note_lines:
        if "[[" in line and "]]" in line:
            line.split("[[")
            line_outgoing_links = re.findall(pattern, line) 
            outgoing_links.extend(line_outgoing_links)
    
    if not outgoing_links:
        return None
    
    outgoing_links = list(set(outgoing_links))
    return outgoing_links