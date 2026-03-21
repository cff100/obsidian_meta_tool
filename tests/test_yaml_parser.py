import pytest

from obsidian_meta_tool.config.paths import TESTS_FILES_FOLDER
from obsidian_meta_tool.frontmatter.yaml_parser import extract_frontmatter, \
                                                       parse_yaml, \
                                                       retrieve_existent_frontmatter, \
                                                       retrieve_yaml_data

from obsidian_meta_tool.frontmatter.yaml_parser import FrontmatterStatus as fe

FRONTMATTER_COMMON_FILE_3 = """
aliases: alias_text
tags:
  - tag/subtag
  - other_tag
"""
FRONTMATTER_DATA_COMMON_FILE_3 = {'aliases': 'alias_text', 'tags': ['tag/subtag', 'other_tag']}
COMMON_FILE_3_PATH = TESTS_FILES_FOLDER / "common_file_3.md"



EXPECTED_FRONTMATTER_COMMON_FILE_1 = """
aliases:
tags:
  - objetivo-uso/ativo
  - mov/meta-organizacao
categorias:
  - "[[Objetivos (Categoria)]]"
objetivo_tipos:
  - "[[Objetivos originais]]"
impacto: 3
progresso_por_foco: 10.5
prazo:
fazer:
status:
  - "[[Em-Desenvolvimento]]"
  - "[[Contínua]]"
progresso: 10
created: 2026-02-23T13:10:01
dia: 2026-03-03
"""


COMMON_FILE_1_PATH = TESTS_FILES_FOLDER / "common_file_1.md"

EMPTY_FILE_PATH = TESTS_FILES_FOLDER / "empty_file.md"

NO_FRONTMATTER_FILE_PATH = TESTS_FILES_FOLDER / "no_frontmatter_file.md"

NO_FRONTMATTER_FILE_2_PATH = TESTS_FILES_FOLDER / "no_frontmatter_file_2.md"

UNCLOSED_FRONTMATTER_FILE_PATH = TESTS_FILES_FOLDER / "unclosed_frontmatter_file.md"
                                      

EMPTY_FRONTMATTER_FILE_PATH = TESTS_FILES_FOLDER / "empty_frontmatter_file.md"                     

class TestRetrieveYamlData:

  def test_valid_file(self):
    assert retrieve_yaml_data(COMMON_FILE_3_PATH) == (fe.VALID, FRONTMATTER_DATA_COMMON_FILE_3)


class TestExtractFrontmatter:

  def test_valid_frontmatter(self):
    """Test extracting frontmatter from a file with valid YAML frontmatter."""

    status, result = extract_frontmatter(COMMON_FILE_1_PATH)
    assert status, result == (fe.VALID, EXPECTED_FRONTMATTER_COMMON_FILE_1)

  def test_no_lines_error(self):
    status, result = extract_frontmatter(EMPTY_FILE_PATH)
    assert status == fe.EMPTY_FILE
    assert result == None

  @pytest.mark.parametrize("path",[NO_FRONTMATTER_FILE_PATH, NO_FRONTMATTER_FILE_2_PATH])
  def test_no_frontmatter_error(self, path):
    status, result = extract_frontmatter(path)
    assert status == fe.MISSING
    assert result == None

  def test_unclosed_frontmatter_error(self):
    status, result = extract_frontmatter(UNCLOSED_FRONTMATTER_FILE_PATH)
    assert status == fe.BROKEN
    assert result == None

  def test_empty_frontmatter_error(self):
    status, result = extract_frontmatter(EMPTY_FRONTMATTER_FILE_PATH)
    assert status == fe.EMPTY
    assert result == None

class TestRetrieveExistentForntmatter:

  @pytest.mark.parametrize("status",[fe.VALID, fe.EMPTY])
  def test_existent_frontmatter(self, status):
    data = retrieve_existent_frontmatter(status, FRONTMATTER_COMMON_FILE_3)
    # print(data)
    assert data == FRONTMATTER_DATA_COMMON_FILE_3

  @pytest.mark.parametrize("status",[fe.MISSING, fe.BROKEN, fe.EMPTY_FILE])
  def test_inexistent_frontmatter(self, status):
    data = retrieve_existent_frontmatter(status, None)
    assert data == None

class TestParseYaml:


  def test_frontmatter_is_None(self):
    data = parse_yaml(None)
    assert data == {}


  def test_dict_data(self):
    data = parse_yaml(FRONTMATTER_COMMON_FILE_3)
    # print(f"\n>> Data: {data}")
    assert data == FRONTMATTER_DATA_COMMON_FILE_3


  def test_yaml_error(self):
    frontmatter = """
      aliases: indented_aliases
    tags:
      - tag/subtag
      - other_tag
    """
    data = parse_yaml(frontmatter)
    assert data == {}

