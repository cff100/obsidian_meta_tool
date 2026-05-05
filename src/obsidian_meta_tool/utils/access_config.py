import configparser
from pathlib import Path

from obsidian_meta_tool.config.paths import CONFIG_INI_PATH
from obsidian_meta_tool.config.constants import ConfigNames



def inicialize_config() -> configparser.ConfigParser:
    """
    :return: Config variable
    :rtype: ConfigParser
    """

    config = configparser.ConfigParser()
    config.read(CONFIG_INI_PATH, encoding='utf-8')
    return config

def auto_access_vault_path(option_vault_name: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION) -> Path:
    """
    :param option_vault_name: The option that specifies the vault to access. Defaults to DEFAULT_VAULT_NAME_OPTION.
    :type option_vault_name: str
    :return: The path to the vault
    :rtype: Path
    """

    vault_name = access_vault_name(option_vault_name)
    return access_vault_path(vault_name)


def access_vault_path(vault_name: str) -> Path:
    """
    Accesses the path of a vault given its name, as specified in the config.ini file. 
    The vault name should be a key in the 'vaults_paths' section of the config.ini file.

    :param vault_name: The name of the vault
    :type vault_name: str
    :return: The path to the vault
    :rtype: Path
    """
    config = inicialize_config()
    vault_path = Path(config[ConfigNames.VAULTS_PATHS][vault_name])
    if vault_path.exists():
        return vault_path
    else:
        raise FileNotFoundError
    

def access_vault_name(option_vault_name: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION):

    config = inicialize_config()
    vault_name = config[ConfigNames.VAULTS_NAMES][option_vault_name]
    return vault_name