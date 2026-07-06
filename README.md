# 🗃️ Obsidian Meta Tool

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Uma ferramenta de automação desenvolvida em Python para gerenciamento, manipulação em massa e integração de metadados em cofres (vaults) do Obsidian.

## 📖 Visão Geral

⚠️ **Atenção:** Ao mesmo tempo que busca ser funcional em si, este é um projeto de estudo de programação, por isso as funcionalidades citadas aqui estão apenas planejadas ou em desenvolvimento modesto.

O **Obsidian Meta Tool** foi criado para simplificar e automatizar a leitura, escrita e organização de propriedades nas notas do Obsidian. Diferente de scripts simples, este projeto permite tratar o vault como uma base de dados, facilitando a edição em massa de frontmatter (YAML), tags, aliases, etc.

Ideal para quem possui cofres grandes e precisa manter a consistência da estrutura de conhecimento de forma programática.

## ✨ Funcionalidades

- **Leitura e Interpretação:** Extração segura de metadados (frontmatter) e conteúdo de arquivos `.md`.
- **Edição em Massa:** Adição, modificação ou remoção de campos personalizados em múltiplas notas simultaneamente.
- **Limpeza e Padronização:** Organização de tags, links e propriedades de acordo com regras pré-definidas.
- **Segurança:** Manipulação de arquivos com tratamento de erros para evitar corrupção do markdown original.

## ⚙️ Requisitos

- Python 3.9 ou superior.
- Acesso de leitura e escrita ao diretório do seu vault do Obsidian.
- Dependências listadas no arquivo `requirements.txt` (ex: `pandas`, `ruamel.yaml`).

## 🚀 Instalação

Clone o repositório e configure um ambiente virtual para isolar as dependências do projeto:

```bash
# 1. Clone o repositório
git clone [https://github.com/cff100/obsidian_meta_tool.git](https://github.com/cff100/obsidian_meta_tool.git)
cd obsidian_meta_tool

# 2. Crie o ambiente virtual
python -m venv .venv

# 3. Ative o ambiente virtual
# No Linux/macOS:
source .venv/bin/activate
# No Windows:
.venv\Scripts\activate

# 4. Instale as dependências
pip install -r requirements.txt
```

## 💻 Uso

⚠️ **Importante:** Como a ferramenta realiza alterações em arquivos locais, é altamente recomendável fazer um backup completo do seu vault antes de testar ou executar operações de edição em massa.

Para mais informações: [cli.py](src/obsidian_meta_tool/cli.py)

### TASK 1: Configuração (do config.ini)

### TASK 2: Mapeamento dos caminhos do vault

## 📄 Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
