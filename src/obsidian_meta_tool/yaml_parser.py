from pathlib import Path
from typing import Optional

from ruamel.yaml import YAML

def extract_frontmatter(path: Path) -> Optional[str]:
    
    with open(path, "r",encoding="utf-8") as file:
        lines = file.readlines()
        
        if not lines or lines[0].strip() != "---":
            return None
        
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "".join(lines[1:i])
            
    return None


def create_yaml_object(frontmatter: Optional[str]) -> Optional[YAML]:

    if frontmatter is None:
        return None
    
    yaml = YAML(typ="safe")

    return yaml


def load_yaml(yaml: Optional[YAML], frontmatter: Optional[str]) -> Optional[dict]:

    if not yaml or not frontmatter:
        return None

    data = yaml.load(frontmatter)

    return data


def yaml_data(path: Path) -> Optional[dict]:
    frontmatter = extract_frontmatter(path)
    yaml = create_yaml_object(frontmatter)
    data = load_yaml(yaml, frontmatter)

    return data


if __name__ == "__main__":
    path = Path("C:\\Users\\caiof\\Desktop\\Criar código que atua no arquivos do obsidian.md")
    data = yaml_data(path)
    print(data)

