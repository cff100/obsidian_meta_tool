
def frontmatter_line_numbers(file_lines: list[str]) -> tuple[int,int]:
 
    check_no_lines_error(file_lines)

    start = None
    end = None
    for i, line in enumerate(file_lines):

        if line.strip() == "---":
            if start == None:
                start = i + 1
            else:
                end = i - 1
                break

    if start == None or end == None or end < start:
        raise ValueError("Não há frontmatter neste arquivo")
        

    return start, end
        

def file_has_lines(file_lines: list[str]) -> bool:
    return len(file_lines) != 0

def check_no_lines_error(file_lines: list[str]):
    if not file_has_lines(file_lines):
        raise ValueError("O arquivo não possui linhas para processar.")
    

if __name__ == "__main__":
    file_lines_1 = ["--- ", "frontmatter ", " ---", "texto", "mais texto "]
    file_lines_8 = ["--- ", "frontmatter ", "mais linhas", "de front", " ---", "texto", "---", "mais texto "]
    file_lines_7 = ["--- ", "frontmatter ", "mais linhas", "de front", " ---", "texto", "mais texto "]
    file_lines_6 = ["--- ", " ---", "texto", "mais texto "]
    file_lines_2 = ["frontmatter ", " ---", "texto", "mais texto "]
    file_lines_3 = ["--- ", "frontmatter ", "texto", "mais texto "]
    file_lines_4 = [""]
    file_lines_5 = []
    print(frontmatter_line_numbers(file_lines_4))