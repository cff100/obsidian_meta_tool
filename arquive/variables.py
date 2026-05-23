from pathlib import Path

from obsidian_meta_tool.io.read import read_lines
from obsidian_meta_tool.config.paths import DataPaths as dp, create_file_paths_document, get_initial_folder_name
from obsidian_meta_tool.frontmatter.yaml_parser import retrieve_yaml_data
from arquive.data_serialization import any_to_text
from obsidian_meta_tool.utils.access_config import access_vault_path


def create_file_path_list(vault_name: str) -> list[str]:
    """
    Create file path list.
    
    :param vault_name: The name of the vault.
    :type vault_name: str
    :return: A list of file paths.
    :rtype: list[str]
    """

    txt_file_paths_document = create_file_paths_document(vault_name)
    
    lines = read_lines(txt_file_paths_document)
    lines_without_newline_character = [line.replace("\n", "") for line in lines]

    return lines_without_newline_character


def create_filename_list(file_paths: list[str]) -> list[str]:
    """
    Create filename list.

    :param: vault_name: The name of the vault.
    :type vault_name: str
    :return: A list of filenames.
    :rtype: list[str]
    """

    filenames_list = [str(Path(file_path).stem) for file_path in file_paths]

    return filenames_list

def create_inicial_folder_name_list(vault_name: str, file_paths: list[str]) -> list[str]:
    """
    Create inicial folder list.

    :param: vault_name: The name of the vault.
    :type vault_name: str
    :return: A list of inicial folders names .
    :rtype: list[str] 
    """

    file_paths = create_file_path_list(vault_name)
    vault_path = access_vault_path(vault_name)

    inicial_folder_name_list = [get_initial_folder_name(file_path, vault_path) for file_path in file_paths]

    return inicial_folder_name_list



def create_extension_list(file_paths: list[str]) -> list[str]:
    """
    Create extension list.

    :param: vault_name: The name of the vault.
    :type vault_name: str
    :return: A list of extensions.
    :rtype: list[str] 
    """

    extensions_list = [str(Path(file_path).suffix) for file_path in file_paths]

    return extensions_list


def create_properties_and_status(file_paths: list[str]) -> tuple[list[str], list[None | dict]]:
    """
    Create properties and status list.

    :param: vault_name: The name of the vault.
    :type vault_name: str
    :return: A tuple of properties and status lists.
    :rtype: tuple[list[str], list[None | dict]]
    """

    file_paths_ = [Path(file_path_str) for file_path_str in file_paths]

    properties_status_list = []
    properties_list = []

    for file_path in file_paths_:
        if file_path.is_file() and file_path.suffix == ".md":
            properties_status, data = retrieve_yaml_data(read_lines(file_path))
            properties_status_list.append(properties_status.value)
        else:
            properties_status, data = None, None
            properties_status_list.append(properties_status)
        properties_list.append(data)

    return properties_status_list, properties_list
        

def create_all_data_dictionary(vault_name: str) -> tuple[dict[str, list], list[str]]:
    
    FILE_PATHS_NAME = "file_paths"
    INICIAL_FOLDERS_NAME = "inicial_folders"
    PROPERTIES_STATUS_NAME = "properties_status"
    PROPERTIES_NAME = "properties"


    functions = [create_file_path_list, create_filename_list, create_inicial_folder_name_list, create_extension_list, create_properties_and_status, create_properties_and_status]
    variables_names = [FILE_PATHS_NAME, "filenames", INICIAL_FOLDERS_NAME, "extensions", PROPERTIES_STATUS_NAME, PROPERTIES_NAME]
    variables = {}
    for i, function in enumerate(functions):
        if i == 0:
            variables[variables_names[i]] = function(vault_name)
        elif variables_names[i] == INICIAL_FOLDERS_NAME:
            variables[variables_names[i]] = function(vault_name, variables[FILE_PATHS_NAME])
        elif variables_names[i] == PROPERTIES_STATUS_NAME:
            variables[variables_names[i]] = function(variables[FILE_PATHS_NAME])[0]
        elif variables_names[i] == PROPERTIES_NAME:
            variables[variables_names[i]] = function(variables[FILE_PATHS_NAME])[1]
        else:
            variables[variables_names[i]] = function(variables[FILE_PATHS_NAME])

    variables: dict[str, list]
    return variables, variables_names

    

def organize_all_data(vault_name: str) -> list[tuple]:
    """
    Organize all data.

    :param: vault_name: The name of the vault.
    :type vault_name: str
    :return: A list of tuples.
    :rtype: list[tuple]
    """

    variables, variables_names = create_all_data_dictionary(vault_name)

    all_data = []

    variables_lists = [variables[x] for x in variables_names]

    for file_path, filename, inicial_folder, extension, properties_status, properties in zip(*variables_lists):
        each_data = tuple([any_to_text(x) for x in [file_path, filename, inicial_folder, extension, properties_status, properties]])
        all_data.append(each_data)

    return all_data
        
