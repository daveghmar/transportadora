import os
import glob
import re

for file in glob.glob("*.html"):
    if file == "index.html":
        continue
    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    # Restoring the text
    content = re.sub(r'placeholder=".*? aqui"', 'placeholder="Código aqui"', content)
    content = re.sub(r'<th>C.*?digo</th>', '<th>Código</th>', content)
    content = re.sub(r'<h4 class="mb-3">.*? Total de', '<h4 class="mb-3">📦 Total de', content)
    content = re.sub(r'">.*? Exportar Excel', '">📊 Exportar Excel', content)
    content = re.sub(r'">.*? Limpar Tudo', '">🗑️ Limpar Tudo', content)
    content = re.sub(r'<th>.*O</th>', '<th>❌</th>', content)
    content = re.sub(r'// .*? pegar hora atual', '// 🕒 pegar hora atual', content)
    content = re.sub(r'salva c.*?digo \+ hora', 'salva código + hora', content)
    content = re.sub(r'N.*?o c', 'Não c', content)
    content = re.sub(r'n.*?o apenas', 'não apenas', content)
    content = re.sub(r'<a href="index\.html" class="botao-voltar">.*?</a>', '<a href="index.html" class="botao-voltar">⬅️</a>', content)
    content = re.sub(r'Total de C.*?digos:', 'Total de Códigos:', content)
    content = re.sub(r"'C.*?digo de Barras'", "'Código de Barras'", content)
    content = re.sub(r"'C.*?digo'", "'Código'", content)
    content = re.sub(r'Nenhum c.*?digo para', "Nenhum código para", content)
    content = re.sub(r'remover este c.*?digo', "remover este código", content)
    content = re.sub(r'todos os c.*?digos', "todos os códigos", content)
    content = re.sub(r'let c.*?digos', "let codigos", content)
    content = re.sub(r'let C.*?digos', "let codigos", content)
    
    # Fix variables like codigosA, codigosB
    content = re.sub(r'c.*?digos([a-zA-Z])', r'codigos\1', content)
    content = re.sub(r'C.*?digos([a-zA-Z])', r'codigos\1', content)
    content = re.sub(r'c.*?digo\b', r'codigo', content)
    content = re.sub(r'C.*?digo\b', r'codigo', content)

    # Some remaining variables might be exactly 'codigos' (no letter suffix)
    # The previous regex catches 'c.*?digos([a-zA-Z])' meaning it misses 'codigos'
    # Actually 'let c.*?digos' handles some of it.
    
    # Just generic variable name fix for 'codigos' when used as an array name
    content = content.replace("códigoA", "codigosA")
    content = content.replace("CódigoA", "codigosA")

    with open(file, "w", encoding="utf-8") as f:
        f.write(content)
