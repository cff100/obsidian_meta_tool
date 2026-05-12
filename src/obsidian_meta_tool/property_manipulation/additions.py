
def add_keys(dictionary: dict, new_pairs_key_value: dict) -> dict:
    for key, value in new_pairs_key_value.items():
        dictionary[key] = value
    return dictionary


    