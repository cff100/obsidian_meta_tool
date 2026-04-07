import sqlite3

from obsidian_meta_tool.config.paths import SQL_DATABASE_PATH
from obsidian_meta_tool.database.create_database import create_database
from obsidian_meta_tool.database.variables import organize_all_data


def update_database(database_path: str = SQL_DATABASE_PATH):
    create_database(database_path)
    all_data = organize_all_data("cognitio_vitae_2")
    insert_values(all_data, database_path)

    print("Database updated.")
    

def insert_values(values: list[tuple], database_path: str = SQL_DATABASE_PATH):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.executemany("INSERT INTO files (filename, filepath, extension, frontmatter_status, frontmatter) VALUES (?, ?, ?, ?, ?)", values)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    update_database()
    