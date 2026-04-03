from typing import Any
from pathlib import Path
import json


def any_to_text(variable: Any) -> str:

    if isinstance(variable, Path):
        variable_text = str(variable)
    elif isinstance(variable, dict):
        variable_text = json.dumps(variable)

    return variable_text

def text_to_any(variable_text: str, type_variable: type) -> Path | dict:

    if type_variable == Path:
        variable = Path(variable_text)
    elif type_variable == dict:
        variable = json.loads(variable_text)

    return variable

