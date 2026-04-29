from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd

from obsidian_meta_tool.config.paths import DataPaths as dp
from obsidian_meta_tool.database.data_serialization import text_to_any
from obsidian_meta_tool.frontmatter.yaml_parser import FrontmatterStatus


def manage_sql_to_df(database_path: str = dp.SQL_DATABASE_PATH, csv_path: Path = dp.GENERAL_DATAFRAME_PATH) -> pd.DataFrame:
    df = sql_to_df(database_path)
    df = df_to_new_types(df)
    save_df_as_csv(df, csv_path)
    return df


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


# ----- Type conversion functions -----


def df_filepath_to_path_object(df: pd.DataFrame) -> pd.DataFrame:
    df["filepath"] = df["filepath"].apply(lambda x: text_to_any(x, Path)) # type: ignore
    return df

def df_frontmatter_to_dict(df: pd.DataFrame) -> pd.DataFrame:
    df["frontmatter"] = df["frontmatter"].apply(lambda x: text_to_any(x, dict) if pd.notna(x) else None) # type: ignore
    return df

def df_frontmatter_status_to_enum(df: pd.DataFrame) -> pd.DataFrame:
    df["frontmatter_status"] = df["frontmatter_status"].apply(lambda x: text_to_any(x, FrontmatterStatus) if pd.notna(x) else None) # type: ignore
    return df


