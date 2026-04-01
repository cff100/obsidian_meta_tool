import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read('src/obsidian_meta_tool/config/config.ini', encoding='utf-8')

# Acessando os valores
pasta_dados = Path(config['vaults_paths']['default_vault'])

print(pasta_dados.exists())