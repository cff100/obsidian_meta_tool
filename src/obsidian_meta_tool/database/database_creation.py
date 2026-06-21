
import json
import pandas as pd 
from pathlib import Path

from obsidian_meta_tool.config.paths import ConfigNames, DataPaths
from obsidian_meta_tool.database.notes_categories_creation import CategoriesNames, ObsidianNote
from obsidian_meta_tool.io.read import read_file_paths
from obsidian_meta_tool.config.config_structuration import auto_access_vault_values, ValuesNames
from obsidian_meta_tool.utils.digit_option import digit_option_creation

def dataframe_creation(vault_option_digit: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION_DIGIT) -> pd.DataFrame:
    """
    Orchestrates the creation of the general Parquet DataFrame from all vault notes.
    """

    vault_option = digit_option_creation(vault_option_digit)
    if vault_option is None:
        raise TypeError("A opção fornecida deve ser um dígito")

    vault_values = auto_access_vault_values(vault_option)
    vault_path = vault_values[ValuesNames.VAULT_PATH.value]
    notes_txt_path = vault_values[ValuesNames.NOTES_TXT_PATH.value]
    
    all_data = get_categories_values_all_notes(vault_path, notes_txt_path, vault_option_digit)

    df = pd.DataFrame(all_data, columns=[c.value for c in CategoriesNames])

    # Garantindo que a pasta do DataFrame exista antes de salvar
    DataPaths.GENERAL_DATAFRAME_PATH.parent.mkdir(parents=True, exist_ok=True)

    # # Converte frontmatter (dict ou None) para JSON string para compatibilidade com Parquet
    # df['note_frontmatter'] = df['note_frontmatter'].apply(
    #     lambda x: json.dumps(x, default=str) if x is not None else None
    # )
    
    save_dataframe_as_parquet(df, DataPaths.GENERAL_DATAFRAME_PATH)
    
    return df


def save_dataframe_as_parquet(df: pd.DataFrame, path: Path) -> None:
    """Saves the pandas DataFrame physically to the specified path."""
    df.to_parquet(path)


def get_categories_values_all_notes(vault_path: Path, notes_txt_path: Path, vault_option_digit: str) -> list[dict]:
    """
    Iterates through all file paths, instantiates ObsidianNote objects, 
    and returns their dictionary representations.
    """
    try:
        all_paths = read_file_paths(notes_txt_path)
    except FileNotFoundError:
        notes_txt_path = DataPaths.capture_vault_file_paths(vault_option_digit)
        all_paths = read_file_paths(notes_txt_path)

    categories_values_list = []

    for note_path in all_paths:
        note = ObsidianNote(note_path, vault_path)
        categories_values_list.append(note.to_dict())
    
    return categories_values_list
        

if __name__ == "__main__":
    df = dataframe_creation()
    print("DataFrame successfully generated. Showing a sample:")
    #print(df.sample(n=min(20, len(df)))) # Previne erros se o cofre tiver menos de 20 notas
    print(df)