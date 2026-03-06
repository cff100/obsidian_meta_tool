import pytest

from obsidian_meta_tool.error_classes import frontmatter_errors as fe
from obsidian_meta_tool.utils.frontmatter_utils import file_has_lines, check_no_lines_error, frontmatter_start, frontmatter_end, frontmatter_line_numbers


list_with_lines = ["one", "two", "three lines"]
list_with_blank_lines = ["",""]
list_without_lines = []


class TestFileHasLines:

    def test_has_lines(self):
        assert file_has_lines(list_with_lines)

    def test_blanks_lines_counts_as_line(self):
        assert file_has_lines(list_with_blank_lines)

    def test_has_empty_file(self):
        assert not file_has_lines(list_without_lines)


class TestCheckNoLinesError:

    def test_no_error_occurs(self):
        check_no_lines_error(list_with_lines)


    def test_error_occurs(self):
        with pytest.raises(fe.NoLinesError) as excinfo:
            check_no_lines_error(list_without_lines)
        # print(f"\n      The error message captured was: '{excinfo.value}' List used: {list_without_lines}")


marker_on_first_line = ["---", "text"]
marker_not_on_first_line = ["text", "---"]
not_marker = ["text","more text"]
empty_frontmatter = ["---","---"]
not_closed_frontmatter = ["---", "text", "end"]


class TestFrontmatterStart:

    @pytest.mark.parametrize("file_lines",[
                                            marker_not_on_first_line, 
                                            not_marker, 
                                            list_with_lines, 
                                            list_with_blank_lines
                                            ])
    def test_no_frontmatter(self, file_lines: list[str]):
        with pytest.raises(fe.NoFrontmatterError) as excinfo:
            frontmatter_start(file_lines)
        # print(f"\n      The error message captured was: '{excinfo.value}' List used: {file_lines}")


    def test_frontmatter_start(self):
        assert frontmatter_start(marker_on_first_line) == 1


class TestFrontmatterEnd:

    @pytest.mark.parametrize("file_lines",[
                                            marker_on_first_line, 
                                            not_marker
                                            ])
    def test_no_end(self, file_lines: list[str]):
        assert frontmatter_end(file_lines) == None
        # print(f"\n      The end line captured was: '{frontmatter_end(file_lines)}' List used: {file_lines}")


    @pytest.mark.parametrize("file_lines, end_line",[
                                            (["text","more text","---"], 1), 
                                            (["text","more text", "last frontmatter line", "---", "final line", "---"], 2)
                                            ])
    def test_has_end(self, file_lines: list[str], end_line: int):
        assert frontmatter_end(file_lines) == end_line
        # print(f"\n      The end line captured was: '{frontmatter_end(file_lines)}' List used: {file_lines}")

class TestFrontmatterLineNumbers:

    def test_frontmatter_not_closed(self):
        with pytest.raises(fe.UnclosedFrontmatterError) as excinfo:
            frontmatter_line_numbers(not_closed_frontmatter)
        # print(f"\n      The error message captured was: '{excinfo.value}' List used: {not_closed_frontmatter}")


    def test_empty_frontmatter(self):
        with pytest.raises(fe.EmptyFrontmatterError) as excinfo:
            frontmatter_line_numbers(empty_frontmatter)
        # print(f"\n      The error message captured was: '{excinfo.value}' List used: {empty_frontmatter}")

    def test_frontmatter_line_numbers(self):
        assert frontmatter_line_numbers(["---", "line 1", "line 2", "---"]) == (1,2)