from pathlib import Path

from obsidian_meta_tool.io.read import read_lines
from obsidian_meta_tool.config.paths import DataPaths as dp
from obsidian_meta_tool.frontmatter.yaml_parser import retrieve_yaml_data
from obsidian_meta_tool.database.data_serialization import any_to_text


def create_file_path_list(vault_name: str) -> list[str]:
    """
    Create file path list.
    
    :param vault_name: The name of the vault.
    :type vault_name: str
    :return: A list of file paths.
    :rtype: list[str]
    """

    txt_file_path = dp.txt_paths_file_name(vault_name)
    dp.capture_vault_file_paths(vault_name)

    lines = read_lines(txt_file_path)
    lines_without_newline_character = [line.replace("\n", "") for line in lines]

    return lines_without_newline_character


def create_filename_list(vault_name: str) -> list[str]:
    """
    Create filename list.

    :param: vault_name: The name of the vault.
    :type vault_name: str
    :return: A list of filenames.
    :rtype: list[str]
    """

    file_paths = create_file_path_list(vault_name)

    filenames_list = [str(Path(file_path).stem) for file_path in file_paths]

    return filenames_list


def create_extension_list(vault_name: str) -> list[str]:
    """
    Create extension list.

    :param: vault_name: The name of the vault.
    :type vault_name: str
    :return: A list of extensions.
    :rtype: list[str] 
    """

    file_paths = create_file_path_list(vault_name)

    extensions_list = [str(Path(file_path).suffix) for file_path in file_paths]

    return extensions_list


def create_properties_and_status(vault_name: str) -> tuple[list[str], list[None | dict]]:
    """
    Create properties and status list.

    :param: vault_name: The name of the vault.
    :type vault_name: str
    :return: A tuple of properties and status lists.
    :rtype: tuple[list[str], list[None | dict]]
    """

    file_paths = [Path(file_path_str) for file_path_str in create_file_path_list(vault_name)]

    properties_status_list = []
    properties_list = []

    for file_path in file_paths:
        if file_path.is_file() and file_path.suffix == ".md":
            properties_status, data = retrieve_yaml_data(file_path)
            properties_status_list.append(properties_status.value)
        else:
            properties_status, data = None, None
            properties_status_list.append(properties_status)
        properties_list.append(data)

    return properties_status_list, properties_list
        

def organize_all_data(vault_name: str) -> list[tuple]:
    """
    Organize all data.

    :param: vault_name: The name of the vault.
    :type vault_name: str
    :return: A list of tuples.
    :rtype: list[tuple]
    """

    file_paths = create_file_path_list(vault_name)
    filenames = create_filename_list(vault_name)
    extensions = create_extension_list(vault_name)
    properties_status_list, properties_list = create_properties_and_status(vault_name)

    all_data = []

    for file_path, filename, extension, properties_status, properties in zip(file_paths, filenames, extensions, properties_status_list, properties_list):
        each_data = tuple([any_to_text(x) for x in [file_path, filename, extension, properties_status, properties]])
        all_data.append(each_data)

    return all_data
        


