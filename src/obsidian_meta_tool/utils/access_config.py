import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read('src/obsidian_meta_tool/config/config.ini', encoding='utf-8')

def access_vault_path(vault_name: str) -> Path:
    """
    Accesses the path of a vault given its name, as specified in the config.ini file. 
    The vault name should be a key in the 'vaults_paths' section of the config.ini file.

    :param vault_name: The name of the vault
    :type vault_name: str
    :return: The path to the vault
    :rtype: Path
    """

    vault_path = Path(config['vaults_paths'][vault_name])
    if vault_path.exists():
        return vault_path
    else:
        raise FileNotFoundError