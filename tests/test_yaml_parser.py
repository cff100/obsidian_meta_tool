import pytest

from obsidian_meta_tool.config.paths import TestsFilesPaths as tfp
from obsidian_meta_tool.config.constants import TestFilesFrontmatters as tff
from obsidian_meta_tool.frontmatter.yaml_parser import extract_frontmatter, \
                                                       parse_yaml, \
                                                       retrieve_existent_frontmatter, \
                                                       retrieve_yaml_data

from obsidian_meta_tool.frontmatter.yaml_parser import FrontmatterStatus as fe


class TestRetrieveYamlData:

    @pytest.mark.parametrize(
        "path, frontmatter_data",
        [
            (tfp.COMMON_FILE_3_PATH, tff.FRONTMATTER_DATA_COMMON_FILE_3),
            (tfp.COMMON_FILE_4_PATH, tff.FRONTMATTER_DATA_COMMON_FILE_4),
        ],
    )
    def test_valid_file(self, path, frontmatter_data):
        assert retrieve_yaml_data(path) == (fe.VALID, frontmatter_data)


class TestExtractFrontmatter:

  def test_valid_frontmatter(self):
    """Test extracting frontmatter from a file with valid YAML frontmatter."""

    status, result = extract_frontmatter(tfp.COMMON_FILE_1_PATH)
    assert status == fe.VALID
    assert result == tff.EXPECTED_FRONTMATTER_COMMON_FILE_1

  def test_no_lines_error(self):
    status, result = extract_frontmatter(tfp.EMPTY_FILE_PATH)
    assert status == fe.EMPTY_FILE
    assert result == None

  @pytest.mark.parametrize("path",[tfp.NO_FRONTMATTER_FILE_PATH, tfp.NO_FRONTMATTER_FILE_2_PATH])
  def test_no_frontmatter_error(self, path):
    status, result = extract_frontmatter(path)
    assert status == fe.MISSING
    assert result == None

  def test_unclosed_frontmatter_error(self):
    status, result = extract_frontmatter(tfp.UNCLOSED_FRONTMATTER_FILE_PATH)
    assert status == fe.BROKEN
    assert result == None

  def test_empty_frontmatter_error(self):
    status, result = extract_frontmatter(tfp.EMPTY_FRONTMATTER_FILE_PATH)
    assert status == fe.EMPTY
    assert result == None

class TestRetrieveExistentForntmatter:

  @pytest.mark.parametrize("status",[fe.VALID, fe.EMPTY])
  def test_existent_frontmatter(self, status):
    data = retrieve_existent_frontmatter(status, tff.FRONTMATTER_COMMON_FILE_3)
    assert data == tff.FRONTMATTER_DATA_COMMON_FILE_3

  @pytest.mark.parametrize("status",[fe.MISSING, fe.BROKEN, fe.EMPTY_FILE])
  def test_inexistent_frontmatter(self, status):
    data = retrieve_existent_frontmatter(status, None)
    assert data == None

class TestParseYaml:


  def test_frontmatter_is_None(self):
    data = parse_yaml(None)
    assert data == {}


  def test_dict_data(self):
    data = parse_yaml(tff.FRONTMATTER_COMMON_FILE_3)
    # print(f"\n>> Data: {data}")
    assert data == tff.FRONTMATTER_DATA_COMMON_FILE_3


  def test_yaml_error(self):
    data = parse_yaml(tff.WRONG_FRONTMATTER_1)
    assert data == {}

