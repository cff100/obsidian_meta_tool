from obsidian_meta_tool.config.paths import TestsFilesPaths as tfp
from obsidian_meta_tool.io.read import read_lines


def test_read_lines():
    assert read_lines(tfp.SIMPLE_FILE_1_PATH) == ['---\n','aliases: alias_text\n', 
                                                 'tags:\n', '  - tag/subtag\n', 
                                                 '  - other_tag\n', '---\n', 
                                                 '\n', 'text']