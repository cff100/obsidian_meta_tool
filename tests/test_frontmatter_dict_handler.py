import pytest

from obsidian_meta_tool.frontmatter.frontmatter_dict_handler import (
    clear_item_in_list,
    clear_item_not_in_list,
)


def test_clear_list_value_basic():
    data = {"tags": ["a", "b", "c"], "other": 1}
    out = clear_item_in_list(data, "tags", "b")
    assert out["tags"] == ["a", "c"]
    assert data["tags"] == ["a", "b", "c"]  # original untouched


def test_clear_list_value_not_present():
    data = {"tags": ["a"]}
    out = clear_item_in_list(data, "tags", "x")
    assert out == data


def test_clear_list_value_unwrap():
    data = {"tags": ["only"]}
    out = clear_item_in_list(data, "tags", "only")
    assert out["tags"] is None


def test_clear_list_value_all():
    data = {"tags": [1, 2, 3]}
    out = clear_item_in_list(data, "tags", "All")
    assert out["tags"] is None


def test_clear_list_value_key_error():
    with pytest.raises(KeyError):
        clear_item_in_list({}, "missing", "x")


def test_clear_list_value_type_error():
    with pytest.raises(TypeError):
        clear_item_in_list({"tags": "not-a-list"}, "tags", "x")


def test_clear_non_list_value():
    d = {"foo": 42}
    out = clear_item_not_in_list(d, "foo")
    assert out["foo"] is None
    assert d["foo"] == 42


def test_clear_non_list_key_error():
    with pytest.raises(KeyError):
        clear_item_not_in_list({}, "foo")
