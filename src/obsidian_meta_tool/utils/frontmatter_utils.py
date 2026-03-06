from typing import Optional

from obsidian_meta_tool.error_classes import frontmatter_errors as fe

def frontmatter_line_numbers(file_lines: list[str]) -> tuple[int,int]:
    """
    :param file_lines: A list whose elements are the lines of a file.
    :type file_lines: list[str]
    :return: Index of the start and end lines, respectively, of the frontmatter (does not consider the '---' markers)
    :rtype: tuple[int, int]
    :raises UnclosedFrontmatterError: If the frontmatter is not properly closed (missing closing '---' marker).
    :raises EmptyFrontmatterError: If the frontmatter is empty (No values between the markers '---').
    """
    check_no_lines_error(file_lines)
    fm_start = frontmatter_start(file_lines)
    fm_end = frontmatter_end(file_lines)
    
    if fm_end is None:
        raise fe.UnclosedFrontmatterError("The frontmatter of the file is not properly closed (missing closing '---' marker).") 
    if fm_end < fm_start:
        raise fe.EmptyFrontmatterError("The frontmatter is empty (No values between the markers '---').")

    return fm_start, fm_end


def check_no_lines_error(file_lines: list[str]):
    """
    :param file_lines: A list whose elements are the lines of a file.
    :type file_lines: list[str]
    :raises NoLinesError: If the file has no lines to process.
    """
    
    if not file_has_lines(file_lines):
        raise fe.NoLinesError("The file has no lines to process.")
    


def frontmatter_start(file_lines: list[str]) -> int:
    """
    :param file_lines: A list whose elements are the lines of a file.
    :type file_lines: list[str]
    :return: Index of the frontmatter start line (after the '---' marker)
    :rtype: int
    :raises NoFrontmatterError: If the file does not have frontmatter.
    """
    # if not file_has_lines(file_lines): # This section has been removed for redundancy. This function will likely only be used in the function `frontmatter_line_numbers`, which already checks if the file has lines and raises an error if it doesn't.
    #     raise ValueError("The file has no lines to process.")
    if file_lines[0].strip() != "---":
        raise fe.NoFrontmatterError("There is no frontmatter in this file.")
    else:
        start = 1
    return start


def frontmatter_end(file_lines: list[str]) -> Optional[int]:
    """
    :param file_lines: A list whose elements are the lines of a file.
    :type file_lines: list[str]
    :return: Index of the frontmatter end line (before the '---' marker)
    :rtype: int
    """
    for i, line in enumerate(file_lines[1:], start=1):
        if line.strip() == "---":
            end = i - 1
            return end
    return None


def file_has_lines(file_lines: list[str]) -> bool:
    """
    :param file_lines: A list whose elements are the lines of a file.
    :type file_lines: list[str]
    :return: `True` if the `file_lines` list has elements, that is, if the file has lines.
    :rtype: bool
    """

    return bool(file_lines)
    
