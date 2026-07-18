
import re
import uuid
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from obsidian_meta_tool.frontmatter.yaml_parser import retrieve_yaml_data
from obsidian_meta_tool.io.read import read_lines
from obsidian_meta_tool.config.constants import FRONTMATTER_ID
from obsidian_meta_tool.frontmatter.yaml_parser import FrontmatterStatus
from obsidian_meta_tool.utils.file_format import is_markdown_file

class CategoriesNames(Enum):
    """Names of the categories used as columns in the general DataFrame."""
    NOTE_PATH = "note_path"
    NOTE_FILENAME = "note_filename"
    NOTE_EXTENSION = "note_extension"
    NOTE_INITIAL_FOLDER_NAME = "note_initial_folder_name"
    NOTE_BODY_TAGS = "note_body_tags"
    NOTE_OUTGOING_LINKS = "note_outgoing_links"
    NOTE_FRONTMATTER_STATUS = "note_frontmatter_status"
    NOTE_FRONTMATTER = "note_frontmatter"


class ObsidianNote:
    """Represents a single note within the Obsidian Vault, encapsulating all its metadata and logic."""

    def __init__(self, note_path: Path, vault_path: Path):
        self.path = note_path
        self.vault_path = vault_path
        
        # Internal state
        self._lines: Optional[list[str]] = None
        
        # Attributes to be populated
        self.frontmatter_status: Optional[FrontmatterStatus] = None
        self.frontmatter: Optional[dict[str, Any]] = None

        if is_markdown_file(self.path):
            self._load_file_data()

    # def is_text_file(self) -> bool:
    #     """Checks if the file is a text file that can be parsed for markdown/YAML."""
    #     text_extensions = {".md", ".txt", ".csv", ".json", ".yaml", ".yml"}
    #     return self.path.suffix.lower() in text_extensions

    def _load_file_data(self) -> None:
        """Reads the file and initializes the frontmatter securely."""
        # self._lines = cast(list[str], read_lines(self.path)) 
        self._lines = read_lines(self.path)
        status, fm, _, _ = retrieve_yaml_data(self._lines)
        
        self.frontmatter_status = status
        self.frontmatter = self._ensure_frontmatter_id(fm)
        self.frontmatter = self._convert_frontmatter_to_serializable()

    def _ensure_frontmatter_id(self, fm: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
        """Ensures the note has an ID in the frontmatter, creating one if missing."""
        if fm is None:
            return None
        
        if FRONTMATTER_ID not in fm:
            fm[FRONTMATTER_ID] = str(uuid.uuid4())
            # Note for the future: Since the ID was generated only in memory here,
            # in the future you will need a method `self.save_frontmatter_to_disk()` 
            # to write this new ID physically to the .md file
        
        return fm
    
    def _convert_frontmatter_to_serializable(self) -> Optional[dict[str, Any]]:
        """Converts the frontmatter to a JSON-serializable format, if necessary."""
        if self.frontmatter is None:
            return None
        
        serializable_fm = {}
        for key, value in self.frontmatter.items():
            if isinstance(value, (str, int, float, bool, type(None))):
                serializable_fm[key] = value
            else:
                # For complex data types, it converts them to a string.
                serializable_fm[key] = str(value)
        
        return serializable_fm

    @property
    def filename(self) -> str:
        return self.path.stem

    @property
    def extension(self) -> str:
        return self.path.suffix

    @property
    def initial_folder_name(self) -> str:
        """
        Gets the first folder name inside the vault. 
        If the note is in the root of the vault, returns '/' to avoid indexing errors.
        """
        relative = self.path.relative_to(self.vault_path)
        if len(relative.parts) > 1:
            return relative.parts[0]
        return "/"

    @property
    def body_tags(self) -> Optional[list[str]]:
        if not self._lines:
            return None

        body_tags = []
        for line in self._lines:
            if "#" in line:
                for expression in line.split():
                    if expression.startswith("#") and len(expression) > 1:
                        body_tags.append(expression[1:])
        
        return list(set(body_tags)) if body_tags else None

    @property
    def outgoing_links(self) -> Optional[list[str]]:
        if not self._lines:
            return None

        outgoing_links = []
        pattern = r"\[\[([^|\]]+)(?:\|[^\]]+)?\]\]"

        for line in self._lines:
            if "[[" in line and "]]" in line:
                outgoing_links.extend(re.findall(pattern, line))
        
        return list(set(outgoing_links)) if outgoing_links else None

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the note's properties to a dictionary mapped strictly to CategoriesNames.
        """

        if self.path.is_dir():
            note_filename = None
            note_extension = None
            note_body_tags = None
            note_outgoing_links = None
            note_frontmatter_status = None
            note_frontmatter = None
        else:
            note_filename = self.filename
            note_extension = self.extension
            if is_markdown_file(self.path):
                note_body_tags = self.body_tags
                note_outgoing_links = self.outgoing_links
                note_frontmatter_status = self.frontmatter_status.value if self.frontmatter_status else None
                note_frontmatter = self.frontmatter
            else:
                note_body_tags = None
                note_outgoing_links = None
                note_frontmatter_status = None
                note_frontmatter = None

        return {
            CategoriesNames.NOTE_PATH.value: str(self.path),
            CategoriesNames.NOTE_INITIAL_FOLDER_NAME.value: self.initial_folder_name,
            CategoriesNames.NOTE_FILENAME.value: note_filename,
            CategoriesNames.NOTE_EXTENSION.value: note_extension,
            CategoriesNames.NOTE_BODY_TAGS.value: note_body_tags,
            CategoriesNames.NOTE_OUTGOING_LINKS.value: note_outgoing_links,
            CategoriesNames.NOTE_FRONTMATTER_STATUS.value: note_frontmatter_status,
            CategoriesNames.NOTE_FRONTMATTER.value: note_frontmatter
        }