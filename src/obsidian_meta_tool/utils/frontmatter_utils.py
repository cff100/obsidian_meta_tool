from typing import Optional


def frontmatter_line_numbers(file_lines: list[str]) -> tuple[int,int]:
    """
    :param file_lines: A list whose elements are the lines of a file.
    :type file_lines: list[str]
    :return: Index of the start and end lines, respectively, of the frontmatter (does not consider the '---' markers)
    :rtype: tuple[int, int]
    """
    check_no_lines_error(file_lines)
    fm_start = frontmatter_start(file_lines)
    fm_end = frontmatter_end(file_lines)
    
    if fm_end == None:
        raise ValueError("The front matter of this file is not properly closed.")
    if fm_end < fm_start:
        raise ValueError("The frontmatter is empty (No values between the markers '---').")

    return fm_start, fm_end


def check_no_lines_error(file_lines: list[str]):
    """
    :param file_lines: A list whose elements are the lines of a file.
    :type file_lines: list[str]
    """
    
    if not file_has_lines(file_lines):
        raise ValueError("The file has no lines to process.")
    


def frontmatter_start(file_lines: list[str]) -> int:
    """
    :param file_lines: A list whose elements are the lines of a file.
    :type file_lines: list[str]
    :return: Index of the frontmatter start line (after the '---' marker)
    :rtype: int
    """
    if not file_has_lines(file_lines):
        raise ValueError("The file has no lines to process.")
    if file_lines[0] != "---":
        raise ValueError("There is no frontmatter in this file.")
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
    for i, line in enumerate(file_lines[1:]):
        if line.strip() == "---":
            end = i - 1
            return end
    return None


def file_has_lines(file_lines: list[str]) -> bool:
    """
    Docstring para file_has_lines

    :param file_lines: A list whose elements are the lines of a file.
    :type file_lines: list[str]
    :return: `True` if the `file_lines` list has elements, that is, if the file has lines.
    :rtype: bool
    """

    return bool(file_lines)
    

if __name__ == "__main__":
    file_lines_1 = ["--- ", "frontmatter ", " ---", "texto", "mais texto "]
    file_lines_8 = ["--- ", "frontmatter ", "mais linhas", "de front", " ---", "texto", "---", "mais texto "]
    file_lines_7 = ["--- ", "frontmatter ", "mais linhas", "de front", " ---", "texto", "mais texto "]
    file_lines_6 = ["--- ", " ---", "texto", "mais texto "]
    file_lines_2 = ["frontmatter ", " ---", "texto", "mais texto "]
    file_lines_3 = ["--- ", "frontmatter ", "texto", "mais texto "]
    file_lines_4 = [""]
    file_lines_5 = []
    print(frontmatter_line_numbers(file_lines_4))