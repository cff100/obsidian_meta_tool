import pytest
from pathlib import Path

from obsidian_meta_tool.frontmatter.yaml_parser import extract_frontmatter, parse_yaml, yaml_data


class TestExtractFrontmatter:
    def test_extract_frontmatter_with_valid_frontmatter(self):
        """Test extracting frontmatter from a file with valid YAML frontmatter."""
        path = Path("tests/test_files/common_file_1.md")
        expected_frontmatter = """aliases:
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
  - "[[〰️]]"
progresso: 10
modified: 2026-02-23T13:11:13
created: 2026-02-23T13:10:01
dia: 2026-03-03
"""
        result = extract_frontmatter(path)
        assert result == expected_frontmatter

    def test_extract_frontmatter_empty_file(self):
        """Test extracting frontmatter from an empty file."""
        path = Path("tests/test_files/empty_file.md")
        result = extract_frontmatter(path)
        assert result == ""

    def test_extract_frontmatter_no_frontmatter(self):
        """Test extracting frontmatter from a file without frontmatter."""
        # Create a temporary file without frontmatter
        temp_path = Path("tests/test_files/no_frontmatter.md")
        temp_path.write_text("This is just content.\nNo frontmatter here.")
        try:
            result = extract_frontmatter(temp_path)
            assert result == ""
        finally:
            temp_path.unlink()


class TestParseYaml:
    def test_parse_yaml_valid(self):
        """Test parsing valid YAML string."""
        yaml_str = "key: value\nlist:\n  - item1\n  - item2"
        expected = {"key": "value", "list": ["item1", "item2"]}
        result = parse_yaml(yaml_str)
        assert result == expected

    def test_parse_yaml_empty(self):
        """Test parsing empty YAML string."""
        yaml_str = ""
        result = parse_yaml(yaml_str)
        assert result == {}

    def test_parse_yaml_invalid(self):
        """Test parsing invalid YAML string."""
        yaml_str = "invalid: yaml: content:"
        # Since it uses safe load, it should return {} if not a dict
        result = parse_yaml(yaml_str)
        assert result == {}

    def test_parse_yaml_not_dict(self):
        """Test parsing YAML that is not a dictionary."""
        yaml_str = "- item1\n- item2"
        result = parse_yaml(yaml_str)
        assert result == {}


class TestYamlData:
    def test_yaml_data_with_frontmatter(self):
        """Test yaml_data with a file containing frontmatter."""
        path = Path("tests/test_files/common_file_1.md")
        result = yaml_data(path)
        assert isinstance(result, dict)
        assert "aliases" in result
        assert result["impacto"] == 3

    def test_yaml_data_empty_file(self):
        """Test yaml_data with an empty file."""
        path = Path("tests/test_files/empty_file.md")
        result = yaml_data(path)
        assert result == {}

    def test_yaml_data_no_frontmatter(self):
        """Test yaml_data with a file without frontmatter."""
        temp_path = Path("tests/test_files/no_frontmatter.md")
        temp_path.write_text("This is just content.\nNo frontmatter here.")
        try:
            result = yaml_data(temp_path)
            assert result == {}
        finally:
            temp_path.unlink()
