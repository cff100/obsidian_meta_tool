from pathlib import Path

from obsidian_meta_tool.io.read import read_lines
from obsidian_meta_tool.config.paths import create_txt_paths_file_name
from obsidian_meta_tool.frontmatter.yaml_parser import retrieve_yaml_data



def create_file_path_list(vault_name: str) -> list[str]:

    txt_file_path = create_txt_paths_file_name(vault_name)

    lines = read_lines(txt_file_path)

    lines_without_newline_character = [line.replace("\n", "") for line in lines]

    return lines_without_newline_character


def create_filename_list(vault_name: str) -> list[str]:

    file_paths = create_file_path_list(vault_name)

    filenames_list = [str(Path(file_path).stem) for file_path in file_paths]

    return filenames_list


def create_extension_list(vault_name: str) -> list[str]:

    file_paths = create_file_path_list(vault_name)

    extensions_list = [str(Path(file_path).suffix) for file_path in file_paths]

    return extensions_list


def create_properties_list_and_status_list(vault_name: str) -> tuple[list[str], list[str]]:

    file_paths = [Path(file_path_str) for file_path_str in create_file_path_list(vault_name)]

    status_list = []
    properties_list = []

    for file_path in file_paths:
        print(file_path)
        if file_path.is_file() and file_path.suffix == ".md":
            print(file_path)
            status, data = retrieve_yaml_data(file_path)
            status_list.append(status.value)
        elif file_path.is_dir():
            print(file_path)
            status, data = None, None
            status_list.append(status)
        else:
            print(file_path.suffix)
        print(f"Debug: data = {data}")
        properties_list.append(data)

    return status_list, properties_list
        





if __name__ == "__main__":
    lista_1 = create_file_path_list("cognitio_vitae_2")
    lista_2 = create_filename_list("cognitio_vitae_2")
    lista_3 = create_extension_list("cognitio_vitae_2")
    lista_4, lista_5 = create_properties_list_and_status_list("cognitio_vitae_2")
    print(lista_1[390:400])
    print(lista_2[390:400])
    print(lista_3[390:400])
    print(lista_4[390:400])
    print(lista_5[390:400])

