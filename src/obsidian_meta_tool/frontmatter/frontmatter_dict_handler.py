from typing import Literal, Any
from copy import deepcopy

def remove_dict_value_list(dictionary: dict, key: str, list_value_to_remove: str | Literal["All"]) -> dict:
    """Remove values from the dictionary when they are in a list."""
    
    dict = deepcopy(dictionary)
    if list_value_to_remove == "All":
        dict.update({key: None})
    else:
        list_items = dict[key]
        list_items.remove(list_value_to_remove)
        dict[key] = list_items

        if len(dict[key]) == 0:
            dict[key] = None
        elif len(dict[key]) == 1:
            dict[key] = list_items[0]

    return dict

def remove_dict_value_other(dictionary: dict, key: str, value_to_remove: Any):
    pass


if __name__ == "__main__":

    from obsidian_meta_tool.frontmatter.yaml_parser import yaml_data
    from pathlib import Path

    path = Path(r"C:\Caio_(fora_do_drive)\Python_Projetos\obsidian_meta_tool\data\arquivo_de_teste_1.md")
    data = yaml_data(path)
    print(data)
    # dict = remove_dict_value_list(data, "tags", "objetivo-uso/ativo")
    # dict = remove_dict_value_list(data, "status", "[[〰️]]")
    #dict = remove_dict_value_list(dict, "status", "[[Em-Desenvolvimento]]")
    # print(dict)
    print(type(data["progresso_por_foco"]))