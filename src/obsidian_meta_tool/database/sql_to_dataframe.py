from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd

from obsidian_meta_tool.config.paths import SQL_DATABASE_PATH

# 1. Cria a conexão (exemplo com SQLite, mas serve para outros)
engine = create_engine(f'sqlite:///{SQL_DATABASE_PATH}')

# 2. Lê uma tabela inteira ou uma query específica
df = pd.read_sql("SELECT * FROM files", engine)


def df_filepath_to_path_object(df: pd.DataFrame) -> pd.DataFrame:
    df["filepath"] = df["filepath"].apply(Path) # type: ignore
    return df
    

if __name__ == "__main__":
    # Exemplo de uso
    print(df.head())  # Exibe as primeiras 5 linhas do DataFrame
    print(df_filepath_to_path_object(df).head())
    print(df_filepath_to_path_object(df).info())