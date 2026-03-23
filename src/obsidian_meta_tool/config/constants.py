
class TestFilesFrontmatters:

    FRONTMATTER_COMMON_FILE_3 = \
'aliases: alias_text\n\
tags:\n\
  - tag/subtag\n\
  - other_tag\n\
'
    FRONTMATTER_DATA_COMMON_FILE_3 = {'aliases': 'alias_text', 'tags': ['tag/subtag', 'other_tag']}

    
    
    EXPECTED_FRONTMATTER_COMMON_FILE_1 = \
'aliases:\n\
tags:\n\
  - objetivo-uso/ativo\n\
  - mov/meta-organizacao\n\
categorias:\n\
  - "[[Objetivos (Categoria)]]"\n\
objetivo_tipos:\n\
  - "[[Objetivos originais]]"\n\
impacto: 3\n\
progresso_por_foco: 10.5\n\
prazo:\n\
fazer:\n\
status:\n\
  - "[[Em-Desenvolvimento]]"\n\
  - "[[Contínua]]"\n\
progresso: 10\n\
created: 2026-02-23T13:10:01\n\
dia: 2026-03-03\n'


    WRONG_FRONTMATTER_1 = \
'    aliases: indented_aliases\n\
tags:\n\
  - tag/subtag\n\
  - other_tag'