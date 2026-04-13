import sqlite3

from obsidian_meta_tool.config.paths import SQL_DATABASE_PATH
from obsidian_meta_tool.database.create_database import create_database
from obsidian_meta_tool.database.variables import organize_all_data


def update_database(database_path: str = SQL_DATABASE_PATH) -> None:
    """
    Update the database with the latest data from the Obsidian vault. 
    This function will create the database if it doesn't exist, and then insert all the organized data into it.
    
    :param database_path: The path to the SQLite database file. Defaults to SQL_DATABASE_PATH.
    :type database_path: str
    :return: None
    :rtype: None
    """
    
    create_database(database_path)
    all_data = organize_all_data("cognitio_vitae_2")
    insert_values(all_data, database_path)

    print("Database updated.")
    

def insert_values(values: list[tuple], database_path: str = SQL_DATABASE_PATH) -> None:
    """
    Insert values into the database. 
    This function will connect to the SQLite database, execute the insert statement, and then close the connection.
    
    :param values: A list of tuples containing the values to be inserted.
    :type values: list[tuple]
    :param database_path: The path to the SQLite database file. Defaults to SQL_DATABASE_PATH.
    :type database_path: str
    :return: None
    :rtype: None
    """

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.executemany("INSERT INTO files (filepath, filename, extension, frontmatter_status, frontmatter) VALUES (?, ?, ?, ?, ?)", values)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    update_database()
    