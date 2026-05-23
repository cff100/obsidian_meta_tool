import sqlite3
from pathlib import Path

from obsidian_meta_tool.config.paths import DataPaths as dp

def create_database(database_path: str = dp.SQL_DATABASE_PATH, replace: bool = False) -> None:
    """
    Creates a SQLite database with a table for storing file metadata if it doesn't already exist.
    If it exists, nothing is done.

    :param database_path: The path where the SQLite database will be created.
    :type database_path: str
    :param replace: A boolean indicating whether to replace the existing database. Defaults to False.
    :type replace: bool
    """

    database_exists = Path(database_path).exists()

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    if database_exists:
        print("Database already exists.")


    if replace:
        cursor.execute("DROP TABLE IF EXISTS files")
        print("Existing database dropped.")

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS files ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT NOT NULL,
                filename TEXT NOT NULL,
                inicial_folder TEXT NOT NULL,
                extension TEXT,
                frontmatter_status TEXT,
                frontmatter TEXT
                )             
                """)
    
    if replace or not database_exists:
        print("New database created.")

    connection.commit()
    connection.close()

