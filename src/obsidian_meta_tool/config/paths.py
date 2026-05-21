from pathlib import Path

from obsidian_meta_tool.config.constants import ConfigNames
from obsidian_meta_tool.utils.access_config import auto_access_vault_values

PROJECT_ROOT_FOLDER = Path(__file__).parents[3]

CONFIG_INI_PATH = "src/obsidian_meta_tool/config/config.ini"


class DataPaths:
    """This class contains the paths to the data files."""

    DATA_FOLDER = PROJECT_ROOT_FOLDER / "data"

    SQL_DATABASE_PATH = str(DATA_FOLDER / "all_files.db")

    CSV_FOLDER = DATA_FOLDER / "csv"

    GENERAL_DATAFRAME_PATH = CSV_FOLDER / "general_dataframe.csv"



    @staticmethod
    def capture_vault_file_paths(vault_option: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION) -> None:
        """
        Captures the paths of all files in the vault and saves them to a .txt file in the data folder. 
        The .txt file is named after the vault, with the suffix '_paths.txt'.

        :param vault_name: The name of the vault whose file paths are to be captured.
        :type vault_name: str
        """


        vault_path, vault_name = auto_access_vault_values(vault_option)
        vault_path = vault_path.resolve()

        txt_file_path = DataPaths.txt_paths_file_name(vault_name)             

        with open(txt_file_path, 'w', encoding='utf-8') as file:
            for item in vault_path.rglob("*"):
                file.write(f"{item}\n")

    @staticmethod
    def txt_paths_file_name(vault_name: str) -> Path:
        """
        Returns the file name for the .txt file that will store the paths of all files in the vault. 
        The file name is created by appending the suffix '_paths.txt' to the vault name.
        
        :param vault_name: The name of the vault.
        :type vault_name: str
        :return: The path to the .txt file.
        :rtype: Path

        """
        
        return DataPaths.DATA_FOLDER / (vault_name + "_paths.txt")
    

class TestsFilesPaths:
    """This class contains the paths to the test files used in the unit tests."""

    TESTS_FILES_FOLDER = PROJECT_ROOT_FOLDER / "tests/test_files"

    SIMPLE_FILE_1_PATH = TESTS_FILES_FOLDER / "simple_file_1.md"

    WRITING_FILE_PATH = TESTS_FILES_FOLDER / "writing_file_1.md"

    COMMON_FILE_1_PATH = TESTS_FILES_FOLDER / "common_file_1.md"

    COMMON_FILE_2_PATH = TESTS_FILES_FOLDER / "common_file_2.md"

    COMMON_FILE_3_PATH = TESTS_FILES_FOLDER / "common_file_3.md"

    COMMON_FILE_4_PATH = TESTS_FILES_FOLDER / "common_file_4.md"

    EMPTY_FILE_PATH = TESTS_FILES_FOLDER / "empty_file.md"

    NO_FRONTMATTER_FILE_PATH = TESTS_FILES_FOLDER / "no_frontmatter_file.md"

    NO_FRONTMATTER_FILE_2_PATH = TESTS_FILES_FOLDER / "no_frontmatter_file_2.md"

    UNCLOSED_FRONTMATTER_FILE_PATH = TESTS_FILES_FOLDER / "unclosed_frontmatter_file.md"
                                        
    EMPTY_FRONTMATTER_FILE_PATH = TESTS_FILES_FOLDER / "empty_frontmatter_file.md"

    GOAL_FILE_1_PATH = TESTS_FILES_FOLDER / "goal_file_1.md"                


def create_file_paths_document(vault_name: str) -> Path:

    txt_file_paths_document = DataPaths.txt_paths_file_name(vault_name)
    DataPaths.capture_vault_file_paths(vault_name)

    return txt_file_paths_document


def get_initial_folder_name(file_path: Path | str, vault_path: Path) -> str:

    if isinstance(file_path, str):
        file_path = Path(file_path)

    inicial_folder_name = file_path.relative_to(vault_path)
    #print(inicial_folder_name)
    inicial_folder_name = inicial_folder_name.parts[0]
    #print(inicial_folder_name)
    inicial_folder_name = str(inicial_folder_name)
    #print(inicial_folder_name)

    return inicial_folder_name

def get_non_md_values_csv(vault_path: Path) -> Path:

    non_md_values_csv = vault_path / "non_md_values.csv"
    return non_md_values_csv


