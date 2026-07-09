import pandas as pd

from obsidian_meta_tool.database.notes_categories_creation import CategoriesNames

def note_path_validation(df: pd.DataFrame) -> bool:
    """
    Validates if the note path is not None.
    """
    return not df[CategoriesNames.NOTE_PATH.value].isnull().any()

def note_filename_validation(df: pd.DataFrame) -> bool:
    """
    Validates if the note filename is not None if extension is .md and if the note filename is None otherwise.
    """
    df_md = df[df[CategoriesNames.NOTE_EXTENSION.value] == ".md"]
    df_non_md = df[df[CategoriesNames.NOTE_EXTENSION.value] != ".md"]

    validated = True

    if df_md[CategoriesNames.NOTE_FILENAME.value].isnull().any():
        print("Validation failed: Some .md files have a None filename.")
        validated = False
    if df_non_md[CategoriesNames.NOTE_FILENAME.value].notnull().any():
        print("Validation failed: Some non-.md files have a non-None filename.")
        validated = False
    return validated
