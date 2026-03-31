import sqlite3
import json
from pathlib import Path

# Usando um banco em memória para facilitar o teste
conexao = sqlite3.connect(':memory:') 
cursor = conexao.cursor()

# 1. Criar a tabela
# Usaremos TEXT para as colunas que vão guardar o Path e o Dicionário
cursor.execute('''
    CREATE TABLE arquivos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        caminho TEXT NOT NULL,
        configuracoes TEXT
    )
''')

# --- Nossos objetos nativos do Python ---
meu_caminho = Path('/documentos/relatorio_2026.pdf')
meu_dicionario = {'tamanho_mb': 2.5, 'autor': 'Ana', 'revisado': True}

# 2. Preparar (Serializar) os dados antes de salvar
caminho_str = str(meu_caminho)
configuracoes_json = json.dumps(meu_dicionario) # Transforma o dict em uma string JSON

# 3. Salvar no banco de dados
cursor.execute(
    "INSERT INTO arquivos (caminho, configuracoes) VALUES (?, ?)", 
    (caminho_str, configuracoes_json)
)
conexao.commit()

# 4. Ler do banco e recriar os objetos Python
print("--- Recuperando os dados ---")
cursor.execute("SELECT caminho, configuracoes FROM arquivos")
resultado = cursor.fetchone() # Pega a primeira (e única) linha

texto_do_caminho = resultado[0]
texto_das_configuracoes = resultado[1]

# Reconstruindo os objetos
caminho_recuperado = Path(texto_do_caminho)
dicionario_recuperado = json.loads(texto_das_configuracoes)

# Comprovando que voltaram a ser objetos do Python
print(f"Objeto Path: {caminho_recuperado} | Tipo: {type(caminho_recuperado)}")
print(f"Objeto Dict: {dicionario_recuperado} | Tipo: {type(dicionario_recuperado)}")

conexao.close()