import sqlite3

from obsidian_meta_tool.config.paths import SQL_DATABASE_PATH


def insert_values(values: list[tuple], database_path: str = SQL_DATABASE_PATH):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.executemany("INSERT INTO files (filename, filepath, frontmatter) VALUES (?, ?, ?)", values)
    connection.commit()
    connection.close()