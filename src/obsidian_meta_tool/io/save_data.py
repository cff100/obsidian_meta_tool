import pandas as pd 
from pathlib import Path


def save_dataframe_as_parquet(df: pd.DataFrame, path: Path) -> None:
    """Saves the pandas DataFrame physically to the specified path."""
    df.to_parquet(path)

def save_dataframe_as_csv(df: pd.DataFrame, path: Path) -> None:
    """Saves the pandas DataFrame physically to the specified path."""
    df.to_csv(path, index=False)