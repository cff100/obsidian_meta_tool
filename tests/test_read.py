from obsidian_meta_tool.config.paths import TESTS_FILES_FOLDER
from obsidian_meta_tool.io.read import read_lines

SIMPLE_FILE_1_PATH = TESTS_FILES_FOLDER / "simple_file_1.md"

def test_read_lines():
    assert read_lines(SIMPLE_FILE_1_PATH) == ['---\n','aliases: alias_text\n', 
                                            'tags:\n', '  - tag/subtag\n', 
                                            '  - other_tag\n', '---\n', '\n', 'text']