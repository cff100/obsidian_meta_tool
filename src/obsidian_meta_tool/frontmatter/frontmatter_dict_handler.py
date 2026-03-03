
from typing import Any, Literal, Dict
from copy import deepcopy


def clear_value(
    data: Dict[str, Any],
    key: str,
    value_to_remove: Any | Literal["All"],
    ) -> Dict[str, list]:

    result = deepcopy(data)

    if key not in result:
        raise KeyError(f"{key!r} not found in dictionary")
    
    current = result[key]

    if isinstance(current, list):
        new = clear_item_in_list(current, value_to_remove)
    else:
        new = clear_item_not_in_list(current, value_to_remove)

    result[key] = new

    return result



def clear_item_in_list(
    current_list: list,
    value_to_remove: Any | Literal["All"],
    ) -> list:
    
    """Return a new dictionary with a list value cleaned up.

    The original ``data`` is never modified.

    * If ``list_value_to_remove`` is ``"All"`` the key is set to ``None``.
    * Otherwise ``data[key]`` must be a :class:`list` and the first occurrence
      of ``list_value_to_remove`` is removed.  After removal we normalise the
      result so that an empty list becomes ``None`` and a single-element list is
      unwrapped to the element itself.

    Raises
    ------
    KeyError
        If the requested ``key`` is not present in ``data``.
    TypeError
        If the value under ``key`` is not a list when ``list_value_to_remove``
        is not ``"All"``.
    """

    if value_to_remove == "All":
        return [None]

    if value_to_remove not in current_list:
        raise ValueError("Value not found in the list.")

    try:
        current.remove(list_value_to_remove)
    except ValueError:
        # value not present, nothing to do
        return result

    if len(current) == 0:
        result[key] = None
    elif len(current) == 1:
        result[key] = current[0]
    else:
        result[key] = current

    return result


def clear_item_not_in_list(data: Dict[str, Any], key: str) -> Dict[str, Any]:
    """Return a copy of ``data`` with ``key`` set to ``None``.

    A convenience wrapper around :func:`clear_list_value` when you simply want
    to clear any value, regardless of its type.
    """
    result: Dict[str, Any] = deepcopy(data)
    if key not in result:
        raise KeyError(f"{key!r} not found in dictionary")
    result[key] = None
    return result


if __name__ == "__main__":

    from obsidian_meta_tool.frontmatter.yaml_parser import yaml_data
    from pathlib import Path

    path = Path(r"C:\Caio_(fora_do_drive)\Python_Projetos\obsidian_meta_tool\data\arquivo_de_teste_1.md")
    data = yaml_data(path)
    print(data)
    # dict = clear_list_value(data, "tags", "objetivo-uso/ativo")
    dict = clear_item_in_list(data, "status", "[[〰️]]")
    #dict = clear_list_value(dict, "status", "[[Em-Desenvolvimento]]")
    print(dict)
    # print(type(data["progresso_por_foco"]))