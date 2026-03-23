from obsidian_meta_tool.config.paths import TestsFilesPaths as tfp
from obsidian_meta_tool.io.write import write_lines


def test_write_lines():
    print(write_lines(tfp.WRITING_FILE_PATH, ["a\n","b"]))
