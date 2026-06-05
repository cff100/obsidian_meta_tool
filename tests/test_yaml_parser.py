import pytest

from obsidian_meta_tool.frontmatter.yaml_parser import (
    FrontmatterStatus,
    frontmatter_line_numbers,
    retrieve_yaml_data
)
from obsidian_meta_tool.errors import frontmatter_errors as fe


# ==============================================================================
# FIXTURES (Reusable Test Data)
# ==============================================================================

@pytest.fixture
def lines_valid_frontmatter():
    """Returns a Markdown note with perfectly valid frontmatter structure and data."""
    return ["---\n", "title: Note\n", "tags: [obsidian]\n", "---\n", "Content\n"]


@pytest.fixture
def lines_empty_frontmatter():
    """Returns a note containing '---' markers but no data lines between them."""
    return ["---\n", "---\n", "Content immediately after\n"]


@pytest.fixture
def lines_missing_frontmatter():
    """Returns a note that does not contain any frontmatter."""
    return ["# Note Title\n", "Text here\n"]


# ==============================================================================
# TESTS FOR: frontmatter_line_numbers
# ==============================================================================

def test_line_numbers_valid(lines_valid_frontmatter):
    """Should return the correct start and end indices of a valid frontmatter's content."""
    assert frontmatter_line_numbers(lines_valid_frontmatter) == (1, 2)


def test_line_numbers_empty_file():
    """Should raise NoLinesError if the provided lines list is empty."""
    with pytest.raises(fe.NoLinesError):
        frontmatter_line_numbers([])


def test_line_numbers_missing_frontmatter(lines_missing_frontmatter):
    """Should raise NoFrontmatterError if the file does not start with the '---' marker."""
    with pytest.raises(fe.NoFrontmatterError):
        frontmatter_line_numbers(lines_missing_frontmatter)


def test_line_numbers_unclosed():
    """Should raise UnclosedFrontmatterError if the closing '---' marker is missing."""
    lines = ["---\n", "title: Missing closing marker\n", "Note content\n"]
    with pytest.raises(fe.UnclosedFrontmatterError):
        frontmatter_line_numbers(lines)


def test_line_numbers_empty_frontmatter(lines_empty_frontmatter):
    """Should raise EmptyFrontmatterError if there are no lines between the markers."""
    with pytest.raises(fe.EmptyFrontmatterError):
        frontmatter_line_numbers(lines_empty_frontmatter)


# ==============================================================================
# TESTS FOR: retrieve_yaml_data
# ==============================================================================

def test_retrieve_valid_yaml(lines_valid_frontmatter):
    """Should parse successfully and return VALID status, the data dict, and correct indices."""
    status, data, start, end = retrieve_yaml_data(lines_valid_frontmatter)
    
    assert status == FrontmatterStatus.VALID
    assert data == {"title": "Note", "tags": ["obsidian"]}
    assert start == 1
    assert end == 2


def test_retrieve_yaml_with_only_comments():
    """Ensures that if the frontmatter contains only comments, it returns an empty dict and VALID status."""
    lines = ["---\n", "# Just a comment\n", "# Another comment\n", "---\n"]
    status, data, start, end = retrieve_yaml_data(lines)
    
    assert status == FrontmatterStatus.VALID
    assert data == {}
    assert start == 1
    assert end == 2


def test_retrieve_broken_yaml_syntax():
    """Should return BROKEN status if the structure exists but the inner YAML has invalid syntax."""
    lines = ["---\n", "invalid_yaml: [unclosed_bracket\n", "---\n"]
    status, data, start, end = retrieve_yaml_data(lines)
    
    assert status == FrontmatterStatus.BROKEN
    assert data is None
    assert start == 1
    assert end == 1


def test_retrieve_empty_file():
    """Should return EMPTY_FILE status and Nones for data/indices if the file has no lines."""
    status, data, start, end = retrieve_yaml_data([])
    assert status == FrontmatterStatus.EMPTY_FILE
    assert data is None
    assert start is None
    assert end is None


def test_retrieve_missing_frontmatter(lines_missing_frontmatter):
    """Should return MISSING status if the file begins with standard markdown text."""
    status, data, start, end = retrieve_yaml_data(lines_missing_frontmatter)
    
    assert status == FrontmatterStatus.MISSING
    assert data is None
    assert start is None
    assert end is None


def test_retrieve_unclosed_frontmatter():
    """Should return BROKEN status if the frontmatter is never closed."""
    lines = ["---\n", "title: Forgot to close\n"]
    status, data, start, end = retrieve_yaml_data(lines)
    
    assert status == FrontmatterStatus.BROKEN
    assert data is None
    assert start is None
    assert end is None


def test_retrieve_empty_frontmatter(lines_empty_frontmatter):
    """Should return EMPTY status, an empty dict, and structural indices if no data is present."""
    status, data, start, end = retrieve_yaml_data(lines_empty_frontmatter)
    
    assert status == FrontmatterStatus.EMPTY
    assert data == {}
    assert start == 1
    assert end == 0  # end < start confirms that the inner content is empty