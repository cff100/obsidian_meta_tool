from typing import Optional

def digit_option_creation(digit_choice: str) -> Optional[str]:

    try:
        if digit_choice.isdigit():
            return f"option_{digit_choice}"
    except AttributeError:
        pass
    return None
        