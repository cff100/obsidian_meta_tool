import sqlite3

from obsidian_meta_tool.config.paths import SQL_DATABASE_PATH

def create_database(database_path: str = SQL_DATABASE_PATH):

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS files ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT NOT NULL,
                filename TEXT NOT NULL,
                extension TEXT,
                frontmatter_status TEXT,
                frontmatter TEXT
                )             
                """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_database()