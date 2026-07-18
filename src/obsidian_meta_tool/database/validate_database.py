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

    df_folders = df[df[CategoriesNames.NOTE_PATH.value].apply(lambda x: Path(x).is_dir())]
    df_files = df[df[CategoriesNames.NOTE_PATH.value].apply(lambda x: Path(x).is_file())]
    df_md_files = df_files[df_files[CategoriesNames.NOTE_EXTENSION.value] == '.md']
    df_non_md = df_files[df_files[CategoriesNames.NOTE_EXTENSION.value] != '.md']

    valid = all([path_validation(df), filename_validation(df_folders, df_files), extension_validation(df_folders, df_files), frontmatter_status_validation(df_md_files, df_non_md)])
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

def filename_validation(df_folders: pd.DataFrame, df_files: pd.DataFrame) -> bool:
    """
    Validates if the note filename is None for folders and if the note filename is not None for files.
    """

    valid = True

    if df_folders[CategoriesNames.NOTE_FILENAME.value].notnull().any():
        print("Validation failed: Some folders have a non-None filename.")
        valid = False

        invalid_folder_filenames_df = df_folders[df_folders[CategoriesNames.NOTE_FILENAME.value].notnull()]
        save_dataframe_as_csv(invalid_folder_filenames_df, DataPaths.DATA_FOLDER / "invalid_folder_filenames.csv")
        
    if df_files[CategoriesNames.NOTE_FILENAME.value].isnull().any():
        print("Validation failed: Some files have a None filename.")
        valid = False

        invalid_file_filenames_df = df_files[df_files[CategoriesNames.NOTE_FILENAME.value].isnull()]
        save_dataframe_as_csv(invalid_file_filenames_df, DataPaths.DATA_FOLDER / "invalid_file_filenames.csv")
        
    return valid

def extension_validation(df_folders: pd.DataFrame, df_files: pd.DataFrame) -> bool:
    """
    Validates if the note extension is None for folders and not None for files.
    """

    valid = True

    if df_folders[CategoriesNames.NOTE_EXTENSION.value].notnull().any():
        print("Validation failed: Some folders have a non-None extension.")
        valid = False

        invalid_folders_df = df_folders[df_folders[CategoriesNames.NOTE_EXTENSION.value].notnull()]
        save_dataframe_as_csv(invalid_folders_df, DataPaths.DATA_FOLDER / "invalid_folders.csv")

    if df_files[CategoriesNames.NOTE_EXTENSION.value].isnull().any():
        print("Validation failed: Some files have a None extension.")
        valid = False

        invalid_files_df = df_files[df_files[CategoriesNames.NOTE_EXTENSION.value].isnull()]
        save_dataframe_as_csv(invalid_files_df, DataPaths.DATA_FOLDER / "invalid_files.csv")
        
    return valid

def frontmatter_status_validation(df_md_files: pd.DataFrame, df_non_md: pd.DataFrame) -> bool:
    """
    Validates if the frontmatter status is one of the valid statuses defined in FrontmatterStatus for .md files and None otherwise.
    """
    valid_statuses = [status.value for status in FrontmatterStatus]
    # invalid_statuses_df = df_md_files[~df_md_files[CategoriesNames.NOTE_FRONTMATTER_STATUS.value].isin(valid_statuses)]

    valid = True
    
    if df_non_md[CategoriesNames.NOTE_FRONTMATTER_STATUS.value].notnull().any():
        print("Validation failed: Some non-markdown files or folders have a non-None frontmatter status.")
        valid = False

        invalid_non_md_df = df_non_md[df_non_md[CategoriesNames.NOTE_FRONTMATTER_STATUS.value].notnull()]
        save_dataframe_as_csv(invalid_non_md_df, DataPaths.DATA_FOLDER / "invalid_non_md_frontmatter_status.csv")

    if df_md_files[CategoriesNames.NOTE_FRONTMATTER_STATUS.value].isin(valid_statuses).all() is False:
        print("Validation failed: Some markdown files have an invalid frontmatter status.")
        valid = False

        invalid_md_df = df_md_files[~df_md_files[CategoriesNames.NOTE_FRONTMATTER_STATUS.value].isin(valid_statuses)]
        save_dataframe_as_csv(invalid_md_df, DataPaths.DATA_FOLDER / "invalid_md_frontmatter_status.csv")

    
    return valid