from tkinter import filedialog, Tk
from typing import Optional, cast, Any
from pathlib import Path
from unidecode import unidecode
import configparser
from enum import Enum

from obsidian_meta_tool.config.constants import ConfigNames
from obsidian_meta_tool.config.paths import DataPaths


CONFIG_INI_PATH = "src/obsidian_meta_tool/config/config.ini"

class ValuesNames(Enum):
    """This class contains the names of the values in the config.ini file."""

    VAULT_PATH = "vault_path"
    VAULT_NAME = "vault_name"
    PRATICAL_VAULT_NAME = "pratical_vault_name"
    NOTES_TXT_PATH = "notes_txt_path"

def process_configuration(bypass_input: bool = False):
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
    notes_txt_path = str(DataPaths.txt_paths_file_name(pratical_vault_name))
    option = choose_config_option(bypass_input)

    values = [vault_path, vault_name, pratical_vault_name, notes_txt_path]
    values = cast(list[str], values)


    values_dictionary = {}
    for name, value in zip(ValuesNames, values):
        values_dictionary[name.value] = value

    save_in_config(values_dictionary, option)


def choose_config_option(bypass_input: bool) -> str:
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
    

def save_in_config(values_dictionary: dict[str, str], option: str) -> None:
    """
    Save the vault path, vault name and pratical vault name in the config.ini file.

    :param option: The option used in config.ini.
    :type option: str
    """

    config = inicialize_config()

    keys_list = list(values_dictionary.keys())

    create_missing_config_categories(config, keys_list)

    for key, value in values_dictionary.items():
        config[key][option] = value

    with open(CONFIG_INI_PATH, 'w') as configfile:
        config.write(configfile)


def create_missing_config_categories(config: configparser.ConfigParser, keys_list: list) -> None:
    """
    To create missing categories in the config.ini file.

    :param config: The config.ini file.
    :type config: configparser.ConfigParser
    """

    is_missing = -1
    
    for category in keys_list:
        if category not in config:

            if is_missing == 0:
                print("There are missing categories in the config.ini file. Creating them...")
                is_missing += 1

            print(f"Creating category {category}")
            config[category] = {}

        
        
        


####### Configuration access


def inicialize_config() -> configparser.ConfigParser:
    
    """
    :return: Config variable
    :rtype: ConfigParser
    """

    config = configparser.ConfigParser()
    config.read(CONFIG_INI_PATH, encoding='utf-8')
    return config

def auto_access_vault_values(vault_option: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION) -> dict[str, Any]:
    """
    Accesses the path of a vault given its representative option, as specified in the config.ini file. 
    The option should be a key in the 'vault_names' section of the config.ini file.

    :param option_vault_name: The option that specifies the vault to access. Defaults to DEFAULT_VAULT_NAME_OPTION.
    :type option_vault_name: str
    :return: The path to the vault
    :rtype: Path
    """
    
    config = inicialize_config()
    if is_config_file_empty(config):
        print("Config file is empty. Starting configuration...")
        process_configuration(True)
        config = inicialize_config()

    vault_path = access_vault_path(config, vault_option)
    vault_name = access_vault_name(config, vault_option)
    notes_txt_path = access_notes_txt_path(config, vault_option)
    pratical_vault_name = access_pratical_vault_name(config, vault_option)

    values = {ValuesNames.VAULT_PATH.value: vault_path, 
              ValuesNames.VAULT_NAME.value: vault_name, 
              ValuesNames.NOTES_TXT_PATH.value: notes_txt_path, 
              ValuesNames.PRATICAL_VAULT_NAME.value: pratical_vault_name
            }

    return values


def is_config_file_empty(config: configparser.ConfigParser) -> bool:
    """
    Checks if the config.ini file is empty.

    :param config: The config.ini file.
    :type config: configparser.ConfigParser
    
    :return: `True` if the config.ini file is empty, `False` otherwise.
    :rtype: bool
    """

    return not bool(config.sections())



def access_vault_path(config: configparser.ConfigParser, vault_option: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION) -> Path:
    """
    Accesses the path of a vault given its name, as specified in the config.ini file. 
    The vault name should be a key in the 'vaults_paths' section of the config.ini file.

    :param vault_name: The name of the vault
    :type vault_name: str
    :return: The path to the vault
    :rtype: Path
    """

    vault_path = Path(config[ValuesNames.VAULT_PATH.value][vault_option])
    if vault_path.exists():
        return vault_path
    else:
        raise FileNotFoundError
    

def access_vault_name(config: configparser.ConfigParser, vault_option: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION):

    vault_name = config[ValuesNames.VAULT_NAME.value][vault_option]
    return vault_name


def access_pratical_vault_name(config: configparser.ConfigParser, vault_option: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION):

    pratical_vault_name = config[ValuesNames.PRATICAL_VAULT_NAME.value][vault_option]
    return pratical_vault_name


def access_notes_txt_path(config: configparser.ConfigParser, vault_option: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION) -> Path:

    notes_txt_path = Path(config[ValuesNames.NOTES_TXT_PATH.value][vault_option])

    return notes_txt_path



