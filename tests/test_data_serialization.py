
from obsidian_meta_tool.database.data_serialization import any_to_text
from obsidian_meta_tool.config.constants import TestFilesFrontmatters as tff


def test_dict_to_text():
    text = any_to_text(tff.FRONTMATTER_DATA_COMMON_FILE_4)
    #print(text)
    assert type(text) == str
