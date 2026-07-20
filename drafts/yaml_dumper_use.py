from pathlib import Path
import datetime

from obsidian_meta_tool.frontmatter.yaml_dumper import replace_data


if __name__ == "__main__":
    # Example usage
    origin = Path("C:\\Users\\caiof\\Drive\\Obsidian\\fabulae\\aaa - Rascunho de vault.md")
    new_frontmatter = {
        "title": ["Updated Note", "hh"],
        "date": datetime.datetime(2026, 6, 6, 15, 30, 45),
        "related": "[[2026-06-06 Note]]"
    }
    fm_start = 1
    fm_end = 5

    replace_data(origin, new_frontmatter, fm_start, fm_end)