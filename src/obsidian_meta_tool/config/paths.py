from pathlib import Path

TESTS_FILES_FOLDER = Path("C:/Caio_(fora_do_drive)/Python_Projetos/" \
                          "obsidian_meta_tool/tests/test_files/")

class TestsFilesPaths:

    SIMPLE_FILE_1_PATH = TESTS_FILES_FOLDER / "simple_file_1.md"

    WRITING_FILE_PATH = TESTS_FILES_FOLDER / "writing_file_1.md"

    COMMON_FILE_1_PATH = TESTS_FILES_FOLDER / "common_file_1.md"

    COMMON_FILE_3_PATH = TESTS_FILES_FOLDER / "common_file_3.md"

    EMPTY_FILE_PATH = TESTS_FILES_FOLDER / "empty_file.md"

    NO_FRONTMATTER_FILE_PATH = TESTS_FILES_FOLDER / "no_frontmatter_file.md"

    NO_FRONTMATTER_FILE_2_PATH = TESTS_FILES_FOLDER / "no_frontmatter_file_2.md"

    UNCLOSED_FRONTMATTER_FILE_PATH = TESTS_FILES_FOLDER / "unclosed_frontmatter_file.md"
                                        
    EMPTY_FRONTMATTER_FILE_PATH = TESTS_FILES_FOLDER / "empty_frontmatter_file.md"                     