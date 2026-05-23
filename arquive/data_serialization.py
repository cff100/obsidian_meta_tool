from typing import Any
from pathlib import Path
import json
import datetime

from obsidian_meta_tool.frontmatter.yaml_parser import FrontmatterStatus


def any_to_text(variable: Any) -> str | None:
    """
    Converts a variable of any type to a string representation for storage in the database.

    :param variable: The variable to be converted to text.
    :type variable: Any
    :return: A string representation of the variable, or None if the variable is None.
    :rtype: str | None
    """

    if isinstance(variable, Path):
        variable_text = str(variable)
    elif isinstance(variable, dict):
        for key, value in variable.items():
            if isinstance(value, datetime.date):
                variable[key] = str(value)
        variable_text = json.dumps(variable)
    elif variable is None:
        variable_text = None
    elif isinstance(variable, str):
        variable_text = variable
    

    return variable_text

def text_to_any(variable_text: str, type_variable: type) -> Path | dict | str | FrontmatterStatus:
    """
    Converts a string representation of a variable back to its original type.
    
    :param variable_text: The string representation of the variable to be converted.
    :type variable_text: str
    :param type_variable: The type to which the variable should be converted.
    :type type_variable: type
    :return: The variable converted back to its original type.
    :rtype: Path | dict
    """

    if type_variable == Path:
        variable = Path(variable_text)
    elif type_variable == dict:
        variable = json.loads(variable_text)
    elif type_variable == FrontmatterStatus:
        variable = FrontmatterStatus(variable_text)
    else:
        variable = variable_text

    return variable

