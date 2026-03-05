import pytest

from obsidian_meta_tool.utils.frontmatter_utils import file_has_lines, check_no_lines_error, frontmatter_start

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
        with pytest.raises(ValueError) as excinfo:
            check_no_lines_error(list_without_lines)
        print(f"\n      The error message captured was: '{excinfo.value}' List used: {list_without_lines}")


marker_on_first_line = ["---"]
marker_not_on_first_line = ["text", "---"]
not_marker = ["text"]


class TestFrontmatterStart:

    @pytest.mark.parametrize("file_lines",[
                                            marker_not_on_first_line, 
                                            not_marker, 
                                            list_with_lines, 
                                            list_with_blank_lines, 
                                            list_without_lines
                                            ])
    def test_error_no_frontmatter(self, file_lines):
        with pytest.raises(ValueError) as excinfo:
            frontmatter_start(file_lines)
        print(f"\n      The error message captured was: '{excinfo.value}' List used: {file_lines}")


    def test_frontmatter_start(self):
        assert frontmatter_start(marker_on_first_line) == 1


# class TestFrontmatterEnd:

