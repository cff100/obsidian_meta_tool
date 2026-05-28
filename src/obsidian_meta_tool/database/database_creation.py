
import pandas as pd 
from pathlib import Path
from typing import cast

from obsidian_meta_tool.config.paths import ConfigNames
from obsidian_meta_tool.database.notes_categories_creation import CategoriesNames, get_all_categories_values
from obsidian_meta_tool.io.read import read_lines
from obsidian_meta_tool.config.config_structuration import auto_access_vault_values


def dataframe_creation(vault_option: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION) -> pd.DataFrame:

    vault_path, notes_txt_path = auto_access_vault_values(vault_option)[0], auto_access_vault_values(vault_option)[2]
    all_data = get_categories_values_all_notes(vault_path, notes_txt_path)

    df = pd.DataFrame(all_data, columns=[c.value for c in CategoriesNames])
    return df


def save_dataframe_as_parquet(df: pd.DataFrame, path: Path) -> None:
    df.to_parquet(path)


def get_categories_values_all_notes(vault_path: Path, notes_txt_path: Path) -> list[dict]:

    all_paths = read_lines(notes_txt_path, without_newline_character=True, as_path=True)
    all_paths = cast(list[Path], all_paths)

    categories_values_list = []
    for note_path in all_paths:
        categories_values = get_all_categories_values(note_path, vault_path)
        categories_values_list.append(categories_values)
    
    categories_values_list = cast(list[dict], categories_values_list)
    return categories_values_list
        
if __name__ == "__main__":
    df = dataframe_creation()
    print(df)