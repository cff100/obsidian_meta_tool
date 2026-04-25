from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd

from obsidian_meta_tool.config.paths import DataPaths as dp
from obsidian_meta_tool.database.data_serialization import text_to_any
from obsidian_meta_tool.frontmatter.yaml_parser import FrontmatterStatus



def sql_to_df(database_path: str = dp.SQL_DATABASE_PATH) -> pd.DataFrame:
    engine = create_engine(f'sqlite:///{database_path}')
    df = pd.read_sql("SELECT * FROM files", engine)
    return df


def df_to_new_types(df: pd.DataFrame) -> pd.DataFrame:
    df = df_filepath_to_path_object(df)
    df = df_frontmatter_to_dict(df)
    df = df_frontmatter_status_to_enum(df)
    return df

def save_df_as_csv(df: pd.DataFrame, csv_path: Path = dp.GENERAL_DATAFRAME_PATH) -> None:
    df.to_csv(csv_path, index=False)


def df_filepath_to_path_object(df: pd.DataFrame) -> pd.DataFrame:
    df["filepath"] = df["filepath"].apply(lambda x: text_to_any(x, Path)) # type: ignore
    return df

def df_frontmatter_to_dict(df: pd.DataFrame) -> pd.DataFrame:
    df["frontmatter"] = df["frontmatter"].apply(lambda x: text_to_any(x, dict) if pd.notna(x) else None) # type: ignore
    return df

def df_frontmatter_status_to_enum(df: pd.DataFrame) -> pd.DataFrame:
    df["frontmatter_status"] = df["frontmatter_status"].apply(lambda x: text_to_any(x, FrontmatterStatus) if pd.notna(x) else None) # type: ignore
    return df




if __name__ == "__main__":
    # Exemplo de uso
    # df = sql_to_df()
    # print(df.head())  # Exibe as primeiras 5 linhas do DataFrame
    # print(df_filepath_to_path_object(df)["extension"].head(20))
    # print(df_filepath_to_path_object(df).info())
    # print(type(df_filepath_to_path_object(df)["filepath"][1]))
    # print(type(df_frontmatter_to_dict(df)["frontmatter"][800]))
    # print(type(df_frontmatter_status_to_enum(df)["frontmatter_status"][800]))
    # print(df.index.values)
    # print(df_frontmatter_status_to_enum(df).info())

    df = sql_to_df()
    df = df_to_new_types(df)
    save_df_as_csv(df)
    print(df.info())

    # pegar um valor de frontmatter de exemplo
    print(df["frontmatter"][800]["dia_da_semana"])