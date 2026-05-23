import uuid
from typing import Optional, Any
from pathlib import Path

# from obsidian_meta_tool.io.write import append_lines
# from obsidian_meta_tool.io.read import csv_reader
from obsidian_meta_tool.config.constants import FRONTMATTER_ID



def create_ID():
    return str(uuid.uuid4())

def add_ID_to_frontmatter(frontmatter: dict[str, Any] | None) -> dict[str, Any] | None:

    if frontmatter == None:
        return frontmatter
    elif FRONTMATTER_ID in list(frontmatter.keys()):
        return frontmatter
    
    id = create_ID()
    frontmatter[FRONTMATTER_ID] = id
    return frontmatter


def get_ID(frontmatter: dict) -> Optional[str]:

    return frontmatter.get(FRONTMATTER_ID)


# Se md, faça
# Se não, retorne None


# Para arquivos não markdown


# class CsvTitle(Enum):
#     PATH = "path"
#     ID = "ID"

# def map_csv(csv_path: Path) -> dict[str, str]:

#     mapping = {}
#     reader = csv_reader(csv_path)

#     for row in reader:
#         mapping[row[CsvTitle.PATH.value]] = row[CsvTitle.ID.value]

#     return mapping


# def note_in_csv(mapping: dict[str, str], note_path: Path):

#     # Se o caminho da nota estiver no mapping -> True
#     # Se o caminho da nota estiver no mapping
#     ## Se o caminho mudou

#     path_list = list(mapping.keys())
#     if note_path in path_list:
#         return True
#     return False

# # def note_name_changed(mapping: dict[str, str], id: str, note_path: Path):
    
# #     # id = mapping.get(str(note_path))
# #     # if not id:
# #     #     id = create_ID()
# #     #     mapping[str(note_path)] = id




# def save_non_markdown_ID(notes_path_list: list[Path], csv_path: Path) -> None:

#     title = CsvTitle.ID.value + ", " + CsvTitle.PATH.value + "\n"
#     append_lines(csv_path, [title])
#     append_lines(csv_path, notes_path_list)


# Para o caso de arquivos .md
## Criar função que gere o ID

# Para o caso de arquivos não markdown
## Definir o caminho do CSV
## Definir os títulos das culunas do csv: caminho, ID
## Usar função que gere o ID
## Escrever o ID no arquivo CSV dado o caminho da nota