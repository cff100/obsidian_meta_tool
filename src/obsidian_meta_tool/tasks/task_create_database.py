
from obsidian_meta_tool.database.create_database import create_database

"""
Parameters:
- database_path: The path to the SQLite database file. Defaults to SQL_DATABASE_PATH.
- replace: A boolean indicating whether to replace the existing database. Defaults to False.
"""

if __name__ == "__main__":
    create_database()