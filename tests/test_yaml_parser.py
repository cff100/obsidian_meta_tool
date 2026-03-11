import pytest
from pathlib import Path

from obsidian_meta_tool.frontmatter.yaml_parser import extract_frontmatter, parse_yaml

from obsidian_meta_tool.frontmatter.yaml_parser import FrontmatterStatus as fe

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


COMMON_FILE_1_PATH = Path("C:/Caio_(fora_do_drive)/Python_Projetos/" \
                          "obsidian_meta_tool/tests/test_files/" \
                          "common_file_1.md")

EMPTY_FILE_PATH = Path("C:/Caio_(fora_do_drive)/Python_Projetos/" \
                      "obsidian_meta_tool/tests/test_files/" \
                      "empty_file.md")

NO_FRONTMATTER_FILE_PATH = Path("C:/Caio_(fora_do_drive)/Python_Projetos/" \
                                "obsidian_meta_tool/tests/test_files/" \
                                "no_frontmatter_file.md")

NO_FRONTMATTER_FILE_2_PATH = Path("C:/Caio_(fora_do_drive)/Python_Projetos/" \
                                  "obsidian_meta_tool/tests/test_files/" \
                                  "no_frontmatter_file_2.md")

UNCLOSED_FRONTMATTER_FILE_PATH = Path("C:/Caio_(fora_do_drive)/Python_Projetos/" \
                                      "obsidian_meta_tool/tests/test_files/" \
                                      "unclosed_frontmatter_file.md")

EMPTY_FRONTMATTER_FILE_PATH = Path("C:/Caio_(fora_do_drive)/Python_Projetos/" \
                                  "obsidian_meta_tool/tests/test_files/" \
                                  "empty_frontmatter_file.md")


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


class TestParseYaml:


  def test_frontmatter_is_None(self):
    data = parse_yaml(None)
    assert data == {}


  def test_dict_data(self):
    frontmatter = """
    aliases: alias_text
    tags:
      - tag/subtag
      - other_tag
    """
    data = parse_yaml(frontmatter)
    # print(f"\n>> Data: {data}")
    assert data == {'aliases': 'alias_text', 'tags': ['tag/subtag', 'other_tag']}


  def test_yaml_error(self):
    frontmatter = """
      aliases: indented_aliases
    tags:
      - tag/subtag
      - other_tag
    """
    data = parse_yaml(frontmatter)
    assert data == {}


    # def test_extract_frontmatter_empty_file(self):
    #     """Test extracting frontmatter from an empty file."""
    #     path = Path("tests/test_files/empty_file.md")
    #     result = extract_frontmatter(path)
    #     assert result == ""

    # def test_extract_frontmatter_no_frontmatter(self):
    #     """Test extracting frontmatter from a file without frontmatter."""
    #     # Create a temporary file without frontmatter
    #     temp_path = Path("tests/test_files/no_frontmatter.md")
    #     temp_path.write_text("This is just content.\nNo frontmatter here.")
    #     try:
    #         result = extract_frontmatter(temp_path)
    #         assert result == ""
    #     finally:
    #         temp_path.unlink()


# class TestParseYaml:
#     def test_parse_yaml_valid(self):
#         """Test parsing valid YAML string."""
#         yaml_str = "key: value\nlist:\n  - item1\n  - item2"
#         expected = {"key": "value", "list": ["item1", "item2"]}
#         result = parse_yaml(yaml_str)
#         assert result == expected

#     def test_parse_yaml_empty(self):
#         """Test parsing empty YAML string."""
#         yaml_str = ""
#         result = parse_yaml(yaml_str)
#         assert result == {}

#     def test_parse_yaml_invalid(self):
#         """Test parsing invalid YAML string."""
#         yaml_str = "invalid: yaml: content:"
#         # Since it uses safe load, it should return {} if not a dict
#         result = parse_yaml(yaml_str)
#         assert result == {}

#     def test_parse_yaml_not_dict(self):
#         """Test parsing YAML that is not a dictionary."""
#         yaml_str = "- item1\n- item2"
#         result = parse_yaml(yaml_str)
#         assert result == {}


# class TestYamlData:
#     def test_yaml_data_with_frontmatter(self):
#         """Test yaml_data with a file containing frontmatter."""
#         path = Path("tests/test_files/common_file_1.md")
#         result = retrieve_yaml_data(path)
#         assert isinstance(result, dict)
#         assert "aliases" in result
#         assert result["impacto"] == 3

#     def test_yaml_data_empty_file(self):
#         """Test yaml_data with an empty file."""
#         path = Path("tests/test_files/empty_file.md")
#         result = retrieve_yaml_data(path)
#         assert result == {}

#     def test_yaml_data_no_frontmatter(self):
#         """Test yaml_data with a file without frontmatter."""
#         temp_path = Path("tests/test_files/no_frontmatter.md")
#         temp_path.write_text("This is just content.\nNo frontmatter here.")
#         try:
#             result = retrieve_yaml_data(temp_path)
#             assert result == {}
#         finally:
#             temp_path.unlink()