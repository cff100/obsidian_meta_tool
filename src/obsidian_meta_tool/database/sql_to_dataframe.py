import pandas as pd
from sqlalchemy import create_engine

from obsidian_meta_tool.config.paths import SQL_DATABASE_PATH

# 1. Cria a conexão (exemplo com SQLite, mas serve para outros)
engine = create_engine(f'sqlite:///{SQL_DATABASE_PATH}')

# 2. Lê uma tabela inteira ou uma query específica
df = pd.read_sql("SELECT * FROM files WHERE extension = '.md'", engine)

print(df.head()) # Exibe as primeiras 5 linhas