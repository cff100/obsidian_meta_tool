
def replace_lines(all_lines: list, replacement_start_line: int, replacement_end_line: int, new_lines: list):
    """
    
    Replaces a range of lines in a list of lines with new lines. 
    The new lines will be inserted starting at the `start_line` and ending at the `end_line`.
    Assumes that the `start_line` and `end_line` are valid indices for the `all_lines` list.

    :param all_lines: The list of lines where the replacement should happen.
    :type all_lines: list
    :param replacement_start_line: The line number where the replacement should start. Indexing starts at 0.
    :type replacement_start_line: int
    :param replacement_end_line: The line number where the replacement should end. 
    :type replacement_end_line: int
    :param new_lines: The list of lines that will replace the old lines.
    :type new_lines: list
    :return: The list of lines with the old lines replaced by the new lines.
    :rtype: list[Any]
    """

    all_lines[replacement_start_line:replacement_end_line + 1] = new_lines
    return all_lines