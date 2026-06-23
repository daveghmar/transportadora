const fs = require('fs');
const path = require('path');

const files = fs.readdirSync(__dirname).filter(f => f.endsWith('.html') && f !== 'index.html');

for (const file of files) {
    let content = fs.readFileSync(file, 'utf8');

    // Fix the variables that got messed up
    content = content.replace(/C[?\uFFFD]digos/gi, 'codigos');
    content = content.replace(/c[?\uFFFD]digo/gi, 'codigo');
    content = content.replace(/cdigo/gi, 'codigo');
    content = content.replace(/Cdigo/gi, 'codigo');

    // Restore text content correctly
    content = content.replace(/placeholder=".*? aqui"/g, 'placeholder="Código aqui"');
    content = content.replace(/<th>C.*?digo<\/th>/gi, '<th>Código</th>');
    content = content.replace(/<h4 class="mb-3">.*? Total de/g, '<h4 class="mb-3">📦 Total de');
    content = content.replace(/">.*? Exportar Excel/g, '">📊 Exportar Excel');
    content = content.replace(/">.*? Limpar Tudo/g, '">🗑️ Limpar Tudo');
    content = content.replace(/<th>.*O<\/th>/g, '<th>❌</th>');
    content = content.replace(/\/\/ .*? pegar hora atual/g, '// 🕒 pegar hora atual');
    content = content.replace(/salva c.*?digo \+ hora/g, 'salva código + hora');
    content = content.replace(/N.*?o c/g, 'Não c');
    content = content.replace(/n.*?o apenas/g, 'não apenas');
    content = content.replace(/<a href="index.html" class="botao-voltar">.*?<\/a>/g, '<a href="index.html" class="botao-voltar">⬅️</a>');

    content = content.replace(/Total de C.*?digos:/g, 'Total de Códigos:');
    content = content.replace(/'C.*?digo de Barras'/g, "'Código de Barras'");
    content = content.replace(/'C.*?digo'/g, "'Código'");
    content = content.replace(/Nenhum c.*?digo para/g, "Nenhum código para");
    content = content.replace(/remover este c.*?digo/g, "remover este código");
    content = content.replace(/todos os c.*?digos/g, "todos os códigos");
    
    fs.writeFileSync(file, content, 'utf8');
}
console.log('Fixed all HTML files.');
