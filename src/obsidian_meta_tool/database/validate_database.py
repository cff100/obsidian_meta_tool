import pandas as pd
from pathlib import Path

from obsidian_meta_tool.database.notes_categories_creation import CategoriesNames
from obsidian_meta_tool.io.save_data import save_dataframe_as_csv
from obsidian_meta_tool.config.paths import DataPaths
from obsidian_meta_tool.frontmatter.yaml_parser import FrontmatterStatus

def validate_database(df: pd.DataFrame) -> bool:
    """
    Validates the database by checking if the note path and note filename are valid.
    """
    valid = all([path_validation(df), filename_validation(df), extension_validation(df), frontmatter_status_validation(df)])
    if valid:
        print("Database validation successful.")
    else:
        print("Database validation failed.")
    return valid

def path_validation(df: pd.DataFrame) -> bool:
    """
    Validates if the note path is not None.
    """
    valid = not df[CategoriesNames.NOTE_PATH.value].isnull().any()
    if not valid:
        print("Validation failed: Some note paths are None.")
        invalid_paths_df = df[df[CategoriesNames.NOTE_PATH.value].isnull()]
        save_dataframe_as_csv(invalid_paths_df, DataPaths.DATA_FOLDER / "invalid_paths.csv")
    return valid

def filename_validation(df: pd.DataFrame) -> bool:
    """
    Validates if the note filename is not None if extension is .md and if the note filename is None otherwise.
    """
    df_md = df[df[CategoriesNames.NOTE_EXTENSION.value] == ".md"]
    df_non_md = df[df[CategoriesNames.NOTE_EXTENSION.value] != ".md"]

    valid = True

    if df_md[CategoriesNames.NOTE_FILENAME.value].isnull().any():
        print("Validation failed: Some .md files have a None filename.")
        valid = False

        invalid_filenames_df = df_md[df_md[CategoriesNames.NOTE_FILENAME.value].isnull()]
        save_dataframe_as_csv(invalid_filenames_df, DataPaths.DATA_FOLDER / "invalid_filenames.csv")
        
    if df_non_md[CategoriesNames.NOTE_FILENAME.value].notnull().any():
        print("Validation failed: Some non-.md files have a non-None filename.")
        valid = False

        invalid_non_md_filenames_df = df_non_md[df_non_md[CategoriesNames.NOTE_FILENAME.value].notnull()]
        save_dataframe_as_csv(invalid_non_md_filenames_df, DataPaths.DATA_FOLDER / "invalid_non_md_filenames.csv")
        
    return valid

def extension_validation(df: pd.DataFrame) -> bool:
    """
    Validates if the note extension is None for folders and not None for files.
    """

    folders_df = df[df[CategoriesNames.NOTE_PATH.value].apply(lambda x: Path(x).is_dir())]
    files_df = df[df[CategoriesNames.NOTE_PATH.value].apply(lambda x: Path(x).is_file())]

    valid = True

    if folders_df[CategoriesNames.NOTE_EXTENSION.value].notnull().any():
        print("Validation failed: Some folders have a non-None extension.")
        valid = False

        invalid_folders_df = folders_df[folders_df[CategoriesNames.NOTE_EXTENSION.value].notnull()]
        save_dataframe_as_csv(invalid_folders_df, DataPaths.DATA_FOLDER / "invalid_folders.csv")

    if files_df[CategoriesNames.NOTE_EXTENSION.value].isnull().any():
        print("Validation failed: Some files have a None extension.")
        valid = False

        invalid_files_df = files_df[files_df[CategoriesNames.NOTE_EXTENSION.value].isnull()]
        save_dataframe_as_csv(invalid_files_df, DataPaths.DATA_FOLDER / "invalid_files.csv")
        
    return valid

def frontmatter_status_validation(df: pd.DataFrame) -> bool:
    """
    Validates if the frontmatter status is either 'valid' or 'invalid'.
    """
    valid_statuses = [status.value for status in FrontmatterStatus]
    invalid_statuses_df = df[~df[CategoriesNames.NOTE_FRONTMATTER_STATUS.value].isin(valid_statuses)]
    
    if not invalid_statuses_df.empty:
        print("Validation failed: Some frontmatter statuses are invalid.")
        save_dataframe_as_csv(invalid_statuses_df, DataPaths.DATA_FOLDER / "invalid_frontmatter_statuses.csv")
        return False
    
    return True