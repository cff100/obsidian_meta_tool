import pytest

ALL_LINES_EXEMPLE = ["---", "aliases:", "tags:", "status:", "day:", "---"]

from obsidian_meta_tool.utils.lines_utils import replace_lines

@pytest.mark.parametrize(["replacement_start_line", "replacement_end_line", "new_lines", "new_all_lines"],[
                        (1, 2,["substitute"], ["---", "substitute", "status:", "day:", "---"]),   # Replaces two properties with one (less lines than the original).
                        (1, 1,["substitute"], ["---", "substitute", "tags:", "status:", "day:", "---"]), # Replaces one property with another (same number of lines).
                        (1, 2,["substitute_1", "substitute_2", "substitute_3"], # Replaces two property with three (More lines than the original).
                            ["---", "substitute_1", "substitute_2", "substitute_3", "status:", "day:", "---"])
                        ])
def test_replace_lines(replacement_start_line, replacement_end_line, new_lines, new_all_lines):
    all_lines = replace_lines(ALL_LINES_EXEMPLE, 
                              replacement_start_line, 
                              replacement_end_line, 
                              new_lines)
    assert all_lines == new_all_lines
