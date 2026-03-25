from typing import cast

from obsidian_meta_tool.frontmatter.yaml_dumper import dump_yaml, replace_data
from obsidian_meta_tool.config.constants import TestFilesFrontmatters as tff
from obsidian_meta_tool.config.paths import TestsFilesPaths as tfp
from obsidian_meta_tool.frontmatter.yaml_parser import retrieve_yaml_data





def test_dump_yaml():
    data_lines = dump_yaml(tff.FRONTMATTER_DATA_COMMON_FILE_3)
    assert data_lines == ["aliases: alias_text\n", "tags:\n", "  - tag/subtag\n", "  - other_tag\n"]


def test_replace_data():
    origin_path = tfp.COMMON_FILE_1_PATH
    _, new_frontmatter = retrieve_yaml_data(tfp.COMMON_FILE_2_PATH)
    new_frontmatter = cast(dict, new_frontmatter)
    goal_path = tfp.GOAL_FILE_1_PATH
    replace_data(origin_path, new_frontmatter, goal_path)
    
    with open(goal_path,"r", encoding="utf-8") as file:
        content = file.read()
    
    assert content == tff.EXPECTED_FRONTMATTER_COMMON_FILE_2





# import tempfile
# from pathlib import Path



# def test_replace_data_with_temp_dir():
#     with tempfile.TemporaryDirectory() as tmpdir:
#         tmpdir_path = Path(tmpdir)
        
#         # Criar arquivo de origem
#         origin = tmpdir_path / "origin.md"
#         origin.write_text("linha1\nlinha2\nlinha3\nlinha4")
        
#         # Definir arquivo de destino
#         goal = tmpdir_path / "goal.md"
        
#         replace_data(
#             origin_path = origin,
#             old_frontmatter_start = 1,
#             old_frontmatter_end = 3,
#             new_data_lines = "nova\nlinha",
#             goal_path = goal
#         )
        
#         # Verificar resultado
#         result = goal.read_text()
#         assert result == "linha1\nnova\nlinha\nlinha4"
    