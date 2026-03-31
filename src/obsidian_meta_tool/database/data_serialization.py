from typing import Any
from pathlib import Path
import json


def any_to_text(variable: Any):

    if isinstance(variable, Path):
        variable_text = str(variable)
    elif isinstance(variable, dict):
        variable_text = json.dumps(variable)

    return variable_text