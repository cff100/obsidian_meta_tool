from pathlib import Path

from obsidian_meta_tool.utils.digit_option import digit_option_creation
from obsidian_meta_tool.config.constants import ConfigNames

PROJECT_ROOT_FOLDER = Path(__file__).parents[3]


class DataPaths:
    """This class contains the paths to the data files and path generation utilities."""

    DATA_FOLDER = PROJECT_ROOT_FOLDER / "data"
    GENERAL_DATAFRAME_PATH = DATA_FOLDER / "general_dataframe.parquet"

    # SQL_DATABASE_PATH = str(DATA_FOLDER / "all_files.db")
    # CSV_FOLDER = DATA_FOLDER / "csv"

    @staticmethod
    def capture_vault_file_paths(vault_option_digit: str = ConfigNames.DEFAULT_VAULT_NAME_OPTION_DIGIT) -> Path:
        """
        Captures the paths of all real files in the vault and saves them to a .txt file. 
        
        :param vault_option: The option used in config.ini to represent the vault.
        :type vault_option: str
        :return: The path to the newly generated .txt file containing the vault paths.
        :rtype: Path
        """
        # Local import to prevent circular dependencies at module initialization
        from obsidian_meta_tool.config.config_structuration import auto_access_vault_values, ValuesNames

        vault_option = digit_option_creation(vault_option_digit)

        if vault_option is None:
            raise TypeError("A opção fornecida deve ser um dígito")

        vault_values = auto_access_vault_values(vault_option)
        vault_path = vault_values[ValuesNames.VAULT_PATH.value].resolve()
        practical_vault_name = vault_values[ValuesNames.PRACTICAL_VAULT_NAME.value]

        DataPaths.DATA_FOLDER.mkdir(parents=True, exist_ok=True)
        txt_file_path = DataPaths.txt_paths_file_name(practical_vault_name)            

        with txt_file_path.open('w', encoding='utf-8') as file:
            for item in vault_path.rglob("*"):
                file.write(f"{item}\n")
                    
        return txt_file_path

    @staticmethod
    def txt_paths_file_name(practical_vault_name: str) -> Path:
        """
        Returns the file name for the .txt file that will store the paths of all files in the vault. 
        
        :param practical_vault_name: The practical name of the vault.
        :type practical_vault_name: str
        :return: The exact Path object for the .txt file.
        :rtype: Path
        """
        return DataPaths.DATA_FOLDER / f"{practical_vault_name}_paths.txt"


# def get_initial_folder_name(file_path: Path | str, vault_path: Path) -> str:

#     if isinstance(file_path, str):
#         file_path = Path(file_path)

#     inicial_folder_name = file_path.relative_to(vault_path)
#     #print(inicial_folder_name)
#     inicial_folder_name = inicial_folder_name.parts[0]
#     #print(inicial_folder_name)
#     inicial_folder_name = str(inicial_folder_name)
#     #print(inicial_folder_name)

#     return inicial_folder_name


# def get_non_md_values_csv(vault_path: Path) -> Path:

#     non_md_values_csv = vault_path / "non_md_values.csv"
#     return non_md_values_csv


# class TestsFilesPaths:
#     """This class contains the paths to the test files used in the unit tests."""

#     TESTS_FILES_FOLDER = PROJECT_ROOT_FOLDER / "tests/test_files"

#     SIMPLE_FILE_1_PATH = TESTS_FILES_FOLDER / "simple_file_1.md"

#     WRITING_FILE_PATH = TESTS_FILES_FOLDER / "writing_file_1.md"

#     COMMON_FILE_1_PATH = TESTS_FILES_FOLDER / "common_file_1.md"

#     COMMON_FILE_2_PATH = TESTS_FILES_FOLDER / "common_file_2.md"

#     COMMON_FILE_3_PATH = TESTS_FILES_FOLDER / "common_file_3.md"

#     COMMON_FILE_4_PATH = TESTS_FILES_FOLDER / "common_file_4.md"

#     EMPTY_FILE_PATH = TESTS_FILES_FOLDER / "empty_file.md"

#     NO_FRONTMATTER_FILE_PATH = TESTS_FILES_FOLDER / "no_frontmatter_file.md"

#     NO_FRONTMATTER_FILE_2_PATH = TESTS_FILES_FOLDER / "no_frontmatter_file_2.md"

#     UNCLOSED_FRONTMATTER_FILE_PATH = TESTS_FILES_FOLDER / "unclosed_frontmatter_file.md"
                                        
#     EMPTY_FRONTMATTER_FILE_PATH = TESTS_FILES_FOLDER / "empty_frontmatter_file.md"

#     GOAL_FILE_1_PATH = TESTS_FILES_FOLDER / "goal_file_1.md"         