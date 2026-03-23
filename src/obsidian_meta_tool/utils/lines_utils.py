
def split_lines(start: int, end: int, lines: list, new_lines: list):
    lines[start:end + 1] = new_lines
    return lines