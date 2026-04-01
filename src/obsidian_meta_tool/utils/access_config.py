import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read('src/obsidian_meta_tool/config/config.ini', encoding='utf-8')

def access_vault_path(vault_name: str) -> Path:

    vault_path = Path(config['vaults_paths'][vault_name])
    if vault_path.exists():
        return vault_path
    else:
        raise FileNotFoundError