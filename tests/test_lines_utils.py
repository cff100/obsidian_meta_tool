import pytest

from obsidian_meta_tool.utils.lines_utils import replace_lines

@pytest.mark.parametrize(["replacement_start_line", "replacement_end_line", "new_lines", "new_all_lines"], [(1, 2,["substitute"])])
def test_replace_lines():
    all_lines = replace_lines(["---", "aliases:", "tags:", "status:", "day:", "---"], 1, 2, ["substitute"])
    assert all_lines == ["---", "substitute", "status:", "---"]
