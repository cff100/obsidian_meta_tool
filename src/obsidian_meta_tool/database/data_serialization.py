from typing import Any
from pathlib import Path
import json
import datetime


def any_to_text(variable: Any) -> str | None:

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

def text_to_any(variable_text: str, type_variable: type) -> Path | dict:

    if type_variable == Path:
        variable = Path(variable_text)
    elif type_variable == dict:
        variable = json.loads(variable_text)

    return variable

