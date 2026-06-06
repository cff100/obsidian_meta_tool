import configparser
from enum import Enum
from pathlib import Path
from tkinter import filedialog, Tk
from typing import Optional, Any
from unidecode import unidecode

from obsidian_meta_tool.config.constants import ConfigNames
from obsidian_meta_tool.config.paths import DataPaths

CONFIG_INI_PATH = Path("src/obsidian_meta_tool/config/config.ini")


class ValuesNames(Enum):
    """This class contains the names of the values in the config.ini file."""

    VAULT_PATH = "vault_path"
    VAULT_NAME = "vault_name"
    PRACTICAL_VAULT_NAME = "practical_vault_name"
    NOTES_TXT_PATH = "notes_txt_path"


def process_configuration(bypass_input: bool = False) -> None:
    """
    Manage the manipulation of the config.ini file.

    :param bypass_input: `True` to automatically choose the default option in config.ini.
    :type bypass_input: bool
    """
    vault_path = select_vault_folder()
    if not vault_path:
        print("No folder was selected. Exiting...")
        return
    
    vault_name, practical_vault_name = get_vault_names(vault_path)
    notes_txt_path = str(DataPaths.txt_paths_file_name(practical_vault_name))
    option = choose_config_option(bypass_input)

    values_dictionary = {
        ValuesNames.VAULT_PATH.value: vault_path,
        ValuesNames.VAULT_NAME.value: vault_name,
        ValuesNames.PRACTICAL_VAULT_NAME.value: practical_vault_name,
        ValuesNames.NOTES_TXT_PATH.value: notes_txt_path
    }

    save_in_config(values_dictionary, option)


def choose_config_option(bypass_input: bool) -> str:
    """
    To choose the option used in config.ini.

    :param bypass_input: `True` to automatically choose the default option.
    :return: The option chosen.
    :rtype: str
    """
    default_option = ConfigNames.DEFAULT_VAULT_NAME_OPTION

    if bypass_input:
        return default_option

    choice = input(f"Do you want to choose an option or use the default? (default = {default_option}) Leave it blank to use the default: ")
    choice = choice.replace(" ", "")
    
    if not choice:
        return default_option
    
    option = input("Which option should be used in config.ini (option_2, option_3, etc)? You can type just the option number (e.g., type 3 to create 'option_3'): ")
    option = option.strip()

    # Se o usuário digitou apenas números (ex: "3"), transforma em "option_3"
    if option.isdigit():
        option = f"option_{option}"
        
    return option


def get_vault_path() -> str:
    """
    Ask the user for the path to the vault.

    :return: The path to the vault.
    :rtype: str
    """
    return input("What is the path to the vault? ").strip()


def select_vault_folder() -> Optional[str]:
    """
    To select the vault folder using a visual dialog.

    :return: The path to the vault or None if cancelled.
    :rtype: str | None
    """
    root = Tk()
    root.withdraw()

    vault_path = filedialog.askdirectory(title="Select a folder", initialdir="/")
    
    # Destroying the root window is crucial to prevent the tkinter process from getting stuck in memory.
    root.destroy() 

    return vault_path if vault_path else None


def get_vault_names(vault_path: str | Path) -> tuple[str, str]:
    """
    To get the vault name and the practical vault name.

    :param vault_path: The path to the vault.
    :type vault_path: str | Path
    :return: The vault name and the practical vault name.
    :rtype: tuple[str, str]
    """
    path_obj = Path(vault_path)
    vault_name = path_obj.name
    practical_vault_name = unidecode(vault_name).replace(" ", "_")

    return vault_name, practical_vault_name
    

def save_in_config(values_dictionary: dict[str, str], option: str) -> None:
    """
    Save the vault path, vault name and practical vault name in the config.ini file.

    :param values_dictionary: Dictionary mapping config keys to their string values.
    :type values_dictionary: dict[str, str]
    :param option: The option used in config.ini.
    :type option: str
    """
    config = initialize_config()
    keys_list = list(values_dictionary.keys())

    create_missing_config_categories(config, keys_list)

    for key, value in values_dictionary.items():
        config[key][option] = value

    CONFIG_INI_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with CONFIG_INI_PATH.open('w', encoding='utf-8') as configfile:
        config.write(configfile)


def create_missing_config_categories(config: configparser.ConfigParser, keys_list: list[str]) -> None:
    """
    To create missing categories in the config.ini file.

    :param config: The config.ini object.
    :type config: configparser.ConfigParser
    :param keys_list: The list of category sections to ensure exist.
    :type keys_list: list[str]
    """
    missing_detected = False
    
    for category in keys_list:
        if category not in config:
            if not missing_detected:
                print("There are missing categories in the config.ini file. Creating them...")
                missing_detected = True

            print(f"Creating category: {category}")
            config[category] = {}


# ==============================================================================
# CONFIGURATION ACCESS
# ==============================================================================

def initialize_config() -> configparser.ConfigParser:
    """
    Initializes and reads the configuration file.

    :return: Config variable
    :rtype: configparser.ConfigParser
    """
    config = configparser.ConfigParser()
    if CONFIG_INI_PATH.exists():
        config.read(CONFIG_INI_PATH, encoding='utf-8')
    return config


def auto_access_vault_values(vault_option: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION) -> dict[str, Any]:
    """
    Accesses the path of a vault given its representative option, as specified in the config.ini file. 

    :param vault_option: The option that specifies the vault to access.
    :type vault_option: str
    :return: A dictionary containing the vault values.
    :rtype: dict[str, Any]
    """
    config = initialize_config()
    
    if is_config_file_empty(config):
        print("Config file is empty or missing. Starting configuration...")
        process_configuration(bypass_input=True)
        # Reload settings after creating
        config = initialize_config()

    vault_path = access_vault_path(config, vault_option)
    vault_name = access_vault_name(config, vault_option)
    notes_txt_path = access_notes_txt_path(config, vault_option)
    practical_vault_name = access_practical_vault_name(config, vault_option)

    return {
        ValuesNames.VAULT_PATH.value: vault_path, 
        ValuesNames.VAULT_NAME.value: vault_name, 
        ValuesNames.NOTES_TXT_PATH.value: notes_txt_path, 
        ValuesNames.PRACTICAL_VAULT_NAME.value: practical_vault_name
    }


def is_config_file_empty(config: configparser.ConfigParser) -> bool:
    """
    Checks if the config.ini file is empty.

    :param config: The config.ini object.
    :type config: configparser.ConfigParser
    :return: `True` if the config.ini file is empty, `False` otherwise.
    :rtype: bool
    """
    return len(config.sections()) == 0


def access_vault_path(config: configparser.ConfigParser, vault_option: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION) -> Path:
    """
    Accesses the path of a vault given its name, as specified in the config.ini file.

    :param config: The config.ini object.
    :type config: configparser.ConfigParser
    :param vault_option: The name of the vault option.
    :type vault_option: str
    :return: The path to the vault
    :rtype: Path
    :raises FileNotFoundError: If the path stored in the config doesn't exist on disk.
    """
    vault_path = Path(config[ValuesNames.VAULT_PATH.value][vault_option])
    if vault_path.exists():
        return vault_path
    
    raise FileNotFoundError(f"The vault path configured does not exist: {vault_path}")
    

def access_vault_name(config: configparser.ConfigParser, vault_option: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION) -> str:
    return config[ValuesNames.VAULT_NAME.value][vault_option]


def access_practical_vault_name(config: configparser.ConfigParser, vault_option: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION) -> str:
    return config[ValuesNames.PRACTICAL_VAULT_NAME.value][vault_option]


def access_notes_txt_path(config: configparser.ConfigParser, vault_option: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION) -> Path:
    return Path(config[ValuesNames.NOTES_TXT_PATH.value][vault_option])