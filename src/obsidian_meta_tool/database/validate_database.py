import pandas as pd
from typing import Optional

from obsidian_meta_tool.database.notes_categories_creation import CategoriesNames

def validate_database(df: pd.DataFrame) -> bool:
    """
    Validates the database by checking if the note path and note filename are valid.
    """
    valid = path_validation(df) and filename_validation(df)
    if valid:
        print("Database validation successful.")
    else:
        print("Database validation failed.")
    return valid

def path_validation(df: pd.DataFrame) -> bool:
    """
    Validates if the note path is not None.
    """
    return not df[CategoriesNames.NOTE_PATH.value].isnull().any()

def filename_validation(df: pd.DataFrame) -> bool:
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

def extension_validation(df: pd.DataFrame) -> tuple[bool, Optional[pd.DataFrame]]:
    """
    Validates if the note extension is None for folders and not None for files.
    """

    folders_df = df[df[CategoriesNames.NOTE_PATH.value].apply(lambda x: x.is_dir())]
    files_df = df[df[CategoriesNames.NOTE_PATH.value].apply(lambda x: x.is_file())]

    if folders_df[CategoriesNames.NOTE_EXTENSION.value].notnull().any():
        print("Validation failed: Some folders have a non-None extension.")
        return False, folders_df[folders_df[CategoriesNames.NOTE_EXTENSION.value].notnull()]
    if files_df[CategoriesNames.NOTE_EXTENSION.value].isnull().any():
        print("Validation failed: Some files have a None extension.")
        return False, files_df[files_df[CategoriesNames.NOTE_EXTENSION.value].isnull()]
    return True, None