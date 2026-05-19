from tkinter import filedialog, Tk
from typing import Optional
from pathlib import Path
from unidecode import unidecode

from obsidian_meta_tool.utils.access_config import inicialize_config
from obsidian_meta_tool.config.constants import ConfigNames
from obsidian_meta_tool.config.paths import CONFIG_INI_PATH


def main(bypass_input: bool = False):
    """
    Manage the manipulation of the config.ini file.

    :param bypass_input: `True` to automatically choose the default option in config.ini.
    :type bypass_input: bool
    """

    vault_path = select_vault_folder()
    if not vault_path:
        print("No folder was selected. Exiting...")
        return
    
    vault_name, pratical_vault_name = get_vault_names(vault_path)
    option = choose_config_option(bypass_input)
    save_in_config(vault_name, pratical_vault_name, vault_path, option)


def choose_config_option(bypass_input) -> str:
    """
    To choose the option used in config.ini.

    :param bypass_input: `True` to automatically choose the default option.
    :return: The option chosen.
    :rtype: str
    """

    DEFAULT_OPTION = ConfigNames.DEFAULT_VAULT_NAME_OPTION

    if bypass_input:
        return DEFAULT_OPTION

    choose = input(f"Do you want to choose an option or use the default? (default = {DEFAULT_OPTION}) Leave it blank to use the default. ")
    choose = choose.replace(" ", "")
    if not choose:
        return DEFAULT_OPTION
    
    option = input("Which option should be used in config.ini (option_1, option_2, etc)? ")
    return option.strip()





def get_vault_path() -> str:
    """
    Ask the user for the path to the vault.

    :return: The path to the vault.
    :rtype: str
    """

    vault_path = input("What is the path to the vault?")

    return vault_path


def select_vault_folder() -> Optional[str]:
    """
    To select the vault folder.

    :return: The path to the vault.
    :rtype: str | None
    """

    root = Tk()
    root.withdraw()

    vault_path = filedialog.askdirectory(title="Select a folder", initialdir="/")

    if vault_path:
        return vault_path
    else:
        return None
    

def get_vault_names(vault_path: str | Path) -> tuple[str, str]:
    """
    To get the vault name and the pratical vault name.

    :param vault_path: The path to the vault.
    :type vault_path: str | Path
    :return: The vault name and the pratical vault name.
    :rtype: tuple[str, str]
    """

    vault_path = Path(vault_path)
    vault_name = vault_path.name
    pratical_vault_name = unidecode(vault_name).replace(" ", "_")

    return vault_name, pratical_vault_name
    

def save_in_config(vault_name: str, pratical_vault_name: str, vault_path: str, option: str) -> None:
    """
    Save the vault path, vault name and pratical vault name in the config.ini file.

    :param vault_name: The name of the vault.
    :type vault_name: str
    :param pratical_vault_name: The pratical name of the vault.
    :type pratical_vault_name: str
    :param vault_path: The path to the vault.
    :type vault_path: str
    :param option: The option used in config.ini.
    :type option: str
    """

    config = inicialize_config()

    create_missing_config_categories(config)

    config[ConfigNames.VAULTS_PATHS][option] = vault_path
    config[ConfigNames.VAULTS_NAMES][option] = vault_name
    config[ConfigNames.PRATICAL_VAULTS_NAMES][option] = pratical_vault_name
    

    with open(CONFIG_INI_PATH, 'w') as configfile:
        config.write(configfile)


def create_missing_config_categories(config) -> None:
    """
    To create missing categories in the config.ini file.

    :param config: The config.ini file.
    :type config: configparser.ConfigParser
    """


    categories = [ConfigNames.VAULTS_PATHS, ConfigNames.PRATICAL_VAULTS_NAMES, ConfigNames.VAULTS_NAMES]

    for category in categories:
        if category not in config:
            config[category] = {}






if __name__ == "__main__":
    main(True)